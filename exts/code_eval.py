from io import StringIO
import discord
from discord.ext import commands
from discord.ext.commands import Context, Cog, Bot
import subprocess
from subprocess import PIPE
import os
import pprint
from code import InteractiveInterpreter
import contextlib
import re
import textwrap
import traceback
import inspect


CODE_TEMPLATE = """
async def _func():
{0}
"""


def find_nth_occurrence(string: str, substring: str, n: int):
    """Return index of `n`th occurrence of `substring` in `string`, or None if not found."""
    index = 0
    for _ in range(n):
        index = string.find(substring, index+1)
        if index == -1:
            return None
    return index


class Interpreter(InteractiveInterpreter):
    def __init__(self, bot: Bot):
        locals_ = {"bot": bot}
        super().__init__(locals_)
    
    async def run(self, code: str, ctx: Context, io: StringIO, *args, **kwargs):
        self.locals["_rvalue"] = []
        self.locals["ctx"] = ctx
        self.locals["print"] = lambda x: io.write(f"{x}\n")
    
        code_io = StringIO()

        
        for line in code.split('\n'):
            code_io.write(f"    {line}\n")
        

        code = CODE_TEMPLATE.format(code_io.getvalue())
        del code_io

        self.runsource(code, *args, **kwargs)

        self.runsource("_rvalue = _func()", *args, **kwargs)

        rvalue = await self.locals["_rvalue"]

        del self.locals["_rvalue"]
        del self.locals["ctx"]
        del self.locals["print"]

        return rvalue


class Eval(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.env = {}
        self.ln = 0
        self.stdout = StringIO()
    
        self.interpreter = Interpreter(bot)


    def _format(self, inp: str, out):
        self._ = out

        res = ""

        if inp.startswith("_ = "):
            inp = inp[4:]

        lines = [line for line in inp.split("\n") if line.strip()]
        if len(lines) != 1:
            lines += [""]

        for i, line in enumerate(lines):
            if i == 0:
                start = f"In [{self.ln}]: "

            else:
                start = "...: ".rjust(len(str(self.ln)) + 7)

            if i == len(lines) - 2:
                if line.startswith("return"):
                    line = line[6:].strip()

            res += (start + line + "\n")

        self.stdout.seek(0)
        text = self.stdout.read()
        self.stdout.close()
        self.stdout = StringIO()

        if text:
            res += (text + "\n")

        if out is None:
            return (res, None)

        res += f"Out[{self.ln}]: "

        if isinstance(out, discord.Embed):
            res += "<Embed>"
            res = (res, out)

        else:
            if (isinstance(out, str) and out.startswith("Traceback (most recent call last):\n")):
                out = "\n" + "\n".join(out.split("\n")[1:])

            if isinstance(out, str):
                pretty = out
            else:
                pretty = pprint.pformat(out, compact=True, width=60)

            if pretty != str(out):
                res += "\n"

            if pretty.count("\n") > 20:
                li = pretty.split("\n")

                pretty = ("\n".join(li[:3])
                          + "\n ...\n"
                          + "\n".join(li[-3:]))

            res += pretty
            res = (res, None)

        return res


    async def _eval(self, ctx: Context, code: str):
        """Eval the input code string & send an embed to the invoking context."""
        self.ln += 1

        if code.startswith("exit"):
            self.ln = 0
            self.env = {}
            return await ctx.send("```Reset history!```")
        
        print(code)

        env = {
            "message": ctx.message,
            "author": ctx.message.author,
            "channel": ctx.channel,
            "guild": ctx.guild,
            "ctx": ctx,
            "self": self,
            "bot": self.bot,
            "inspect": inspect,
            "discord": discord,
            "contextlib": contextlib
        }

        self.env.update(env)

        # Ignore this code, it works
        code_ = """
async def func():
    try:
        with contextlib.redirect_stdout(self.stdout):
            {}
        if '_' in locals():
            if inspect.isawaitable(_):
                _ = await _
            return _
    finally:
        self.env.update(locals())
""".format(code)
        print(code_)

        try:
            exec(code_, self.env)
            func = self.env['func']
            res = await func()

        except Exception:
            res = traceback.format_exc()

        out, embed = self._format(code, res)
        out = out.rstrip("\n")  # Strip empty lines from output

        # Truncate output to max 15 lines or 1500 characters
        newline_truncate_index = find_nth_occurrence(out, "\n", 15)

        if newline_truncate_index is None or newline_truncate_index > 1500:
            truncate_index = 1500
        else:
            truncate_index = newline_truncate_index

        if len(out) > truncate_index:
            await ctx.send(
                f"```\n{out[:truncate_index]}\n```"
                f"... response truncated;",
                embed=embed
            )
            return

        await ctx.send(f"```\n{out}```", embed=embed)


    @commands.command(aliases=['e', 'eva', 'code', 'evalcode', 'py', 'python'])
    async def eval(self, ctx: Context, *, code: str):
        if ctx.message.author.id == 419022467210936330:
            if '```py' in code or '```python' in code:
                code = "".join(code.split('\n')[:1])

            code = code.strip('`')

            banned_elems = [
                'os',
                'system',
                'chdir',
                'subprocess',
                'urllib',
                'urlopen',
                'while',
                'sys'
            ]

            for elem in banned_elems:
                if elem in code:
                    await ctx.send(':x: Banned element discovered in codeblock!')
                    return

            await self._eval(ctx, code)
        
        else:
            await ctx.send('Uh-oh! You\'re not allowed to use that command!')




def setup(bot):
    bot.add_cog(Eval(bot))
