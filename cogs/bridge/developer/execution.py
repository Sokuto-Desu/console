from common import formatters

async def evaluate(data):
	try:
		result = eval(data)
	except SyntaxError:
		result = await eval(data)
	except Exception as e:
		result = f"```\n{formatters.get_traceback(e)}```"
	
	return result

async def execute(data, _self, bot, ctx):
	# splits data by lines and tabs them (so that _execute() will work)
	tabbed_code = "\n\t" + "\n\t".join(data.split("\n")) 
	# for convenience ¯\_(ツ)_/¯
	formatted_code = tabbed_code.replace("dprint", "await ctx.send") 
	
	# gives access to the main variables in the local exec field
	exec_globals = globals().update(
		{
			"self": _self,
			"bot": bot,
			"ctx": ctx,
			"formatted_code": formatted_code
		}
	)
	
	try:
		exec(
			f"async def _execute():" 
			f"{formatted_code}",
			exec_globals, 
			locals()
		)
		
		await locals()["_execute"]()
	except Exception as e:
		await formatters.reply(ctx, f"```\n{formatters.get_traceback(e)}")