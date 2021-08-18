import subprocess
from subprocess import Popen
import discord
from discord.ext import commands
import requests
import os
import traceback
import time
# import json

supportedImage = [".bmp", ".gif", ".gif87", ".ico", ".icon",
    ".jpe", ".jpeg", ".jpg", ".jp2", ".jps", ".png", ".apng",
    ".tiff", ".pbm", ".webp", ".webm", ".mpg", ".3gp",
    ".mp4", ".mov", ".wmv", ".flv", ".avi", ".mkv"]


class Convert(commands.Cog):
    """Used to convert things"""

    def __init__(self, bot):
        self.bot = bot

    def check_dir(self):
        if not os.path.isdir("downloads"):
            os.mkdir("downloads")
        if not os.path.isdir("senpai_converted_downloads"):
            os.mkdir("senpai_converted_downloads")
        return

    def ffmpeg_img(self, fileName, newFileName, crop, pixfmt, scale):
        command = [
            'ffmpeg',
            '-y',
            '-i',
            fileName,
        ]
        if crop is not None or scale is not None:
            command.append('-vf')
            if crop is not None:
                command.append('crop=' + crop)
            if scale is not None:
                command.append('crop=' + scale)
        if pixfmt is not None:
            command.append('-pix_fmt')
            command.append(pixfmt)
        command.append(newFileName)
        try:
            proc = Popen(command)
            proc.wait()
        except Exception:
            return 1
        return 0

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def convert(self, ctx):
        """
        Group of comamands that convert images or videos to another format
        """
        await ctx.send_help(ctx.command)

    @convert.command(name="unlaunch", aliases=["unlaunchbg"])
    async def unlaunch_background(self, ctx, filelink=None):
        """
        Convert an attachment or linked image to an Unlaunch GIF file
        """

        self.check_dir()
        supported = False
        if filelink is None:
            if ctx.message.attachments:
                f = ctx.message.attachments[0]

                for extension in supportedImage:
                    if f.filename.lower().endswith(extension):
                        supported = True
                        r = requests.get(f.url, allow_redirects=True)
                        fileName = "downloads/" + f.filename
            else:
                await ctx.send_help(ctx.command)
                return
        else:
            for extension in supportedImage:
                if filelink.lower().endswith(extension):
                    r = requests.get(filelink, allow_redirects=True)
                    if filelink.find('/'):
                        fileName = "downloads/" + filelink.rsplit('/', 1)[1]
                    supported = True

        if supported:
            start_time = time.time()
            async with ctx.typing():
                outputtext = await ctx.send("`Downloading image...`")
                try:
                    open(fileName, 'wb').write(r.content)
                except Exception:
                    await outputtext.edit(content="`Failed to download image`")
                    return
                await outputtext.edit(content="`Image downloaded...`")
                newFileName = "downloads/senpai_converted_" + fileName[10:] + "_.gif"
                await outputtext.edit(content="`Converting to GIF...`")
                try:
                    proc = Popen(["ffmpeg", "-i", fileName, "-vf", "crop='if(gte(ih,iw*3/4),iw,ih)':'if(gte(ih,iw*3/4),iw*3/4,ih*3/4)',scale=256:192:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse", "-frames", "1", newFileName])
                    proc.wait()
                except Exception:
                    error_message = traceback.format_exc()
                    print(error_message)
                    await outputtext.edit(content="`Failed to convert to GIF`")
                    return
                await outputtext.edit(content="`Converted to GIF...`")
                await outputtext.edit(content="`Colour Mapping GIF...`")
                try:
                    proc = Popen(["gifsicle", newFileName, "-O3", "--no-extensions", "-k", "24", "#0", "-o", newFileName])
                    proc.wait()
                except Exception:
                    error_message = traceback.format_exc()
                    print(error_message)
                    await outputtext.edit(content="`Failed to map GIF colour...`")
                    return
                await outputtext.edit(content="`GIF colour mapped...`")
                await outputtext.edit(contents="`Optimising GIF size...`")
                warning = False
                x = 0
                while x <= 300 and os.stat(newFileName).st_size > 15000:
                    proc = Popen(["gifsicle", newFileName, "-O3", "--no-extensions", f"--lossy={x}", "-o", newFileName])
                    proc.wait()
                    x += 50
                if os.stat(newFileName).st_size > 15000:
                    warning = True
                await outputtext.edit(contents="`GIF size optimised`")
                await outputtext.edit(contents="`Uploading GIF...`")
                await ctx.send(file=discord.File(newFileName), reference=ctx.message)
                os.remove(fileName)
                os.remove(newFileName)
                await outputtext.edit(content="`All done! Completed in " + str(round(time.time() - start_time, 2)) + " seconds`")
                if warning:
                    await ctx.send("`[Warning] : File size was not reduced to less than 15KiB.\n[Warning] : Converted GIF won't work with Unlaunch (try something less complicated)`")
                return
        else:
            await ctx.send("Unsupported image format, or URL does not end in " + ", ".join(supportedImage))

    @convert.command()
    async def bmp(self, ctx, filelink=None):
        """
        Converts an attached, or linked, image to BMP
        """
        self.check_dir()
        supported = False
        if filelink is None:
            if ctx.message.attachments:
                f = ctx.message.attachments[0]

                for extension in supportedImage:
                    if f.filename.lower().endswith(extension):
                        supported = True
                        r = requests.get(f.url, allow_redirects=True)
                        fileName = "downloads/" + f.filename
            else:
                await ctx.send_help(ctx.command)
                return
        else:
            for extension in supportedImage:
                if filelink.lower().endswith(extension):
                    r = requests.get(filelink, allow_redirects=True)
                    if filelink.find('/'):
                        fileName = "downloads/" + filelink.rsplit('/', 1)[1]
                    supported = True

        if supported:
            start_time = time.time()
            async with ctx.typing():
                outputtext = await ctx.send("`Downloading image...`")
                try:
                    open(fileName, 'wb').write(r.content)
                except Exception:
                    await outputtext.edit(content="`Failed to download image`")
                    return
                await outputtext.edit(content="`Image downloaded...`")
                if not fileName.endswith('.bmp'):
                    await outputtext.edit(content="`Converting to BMP...`")
                    newFileName = "senpai_converted_" + fileName + "_.bmp"
                    err = self.ffmpeg_img(fileName, newFileName, None, "RGB565", None)
                    if err == 1:
                        await outputtext.edit(content="`Failed to convert to BMP`")
                        return
                    await outputtext.edit(content="`Converted to BMP`")
                    await outputtext.edit(content="`Uploading BMP...`")
                    await ctx.send(file=discord.File(newFileName), reference=ctx.message)
                    await outputtext.edit(content="`All done! Completed in " + str(round(time.time() - start_time, 2)) + " seconds`")
                    os.remove(fileName)
                    os.remove(newFileName)
                    return
                else:
                    await outputtext.edit(content="`You asked me to convert a BMP into a ... BMP`")
                    return
        else:
            await ctx.send("`Unsupported image format, or URL does not end in " + ", ".join(supportedImage) + "`")

    @convert.command()
    async def png(self, ctx, filelink=None):
        """
        Converts an attached, or linked, image to PNG
        """
        self.check_dir()
        supported = False
        if filelink is None:
            if ctx.message.attachments:
                f = ctx.message.attachments[0]

                for extension in supportedImage:
                    if f.filename.lower().endswith(extension):
                        supported = True
                        r = requests.get(f.url, allow_redirects=True)
                        fileName = "downloads/" + f.filename
            else:
                await ctx.send_help(ctx.command)
                return
        else:
            for extension in supportedImage:
                if filelink.lower().endswith(extension):
                    r = requests.get(filelink, allow_redirects=True)
                    if filelink.find('/'):
                        fileName = "downloads/" + filelink.rsplit('/', 1)[1]
                    supported = True

        if supported:
            start_time = time.time()
            async with ctx.typing():
                outputtext = await ctx.send("`Downloading image...`")
                try:
                    open(fileName, 'wb').write(r.content)
                except Exception:
                    await outputtext.edit(content="`Failed to download image `")
                    return
                await outputtext.edit(content="`Image downloaded...`")
                if not fileName.endswith('.png'):
                    await outputtext.edit(content="`Converting to PNG...`")
                    newFileName = "senpai_converted_" + fileName + "_.png"
                    err = self.ffmpeg_img(fileName, newFileName, None, None, None)
                    if err == 1:
                        await outputtext.edit(content="`Failed to convert to PNG`")
                        return
                    await outputtext.edit(content="`Converted to PNG`")
                    await outputtext.edit(content="`Uploading PNG...`")
                    await ctx.send(file=discord.File(newFileName), reference=ctx.message)
                    await outputtext.edit(content="`All done! Completed in " + str(round(time.time() - start_time, 2)) + " seconds`")
                    os.remove(fileName)
                    os.remove(newFileName)
                    return
                else:
                    await outputtext.edit(content="`You asked me to convert a PNG into a ... PNG`")
                    return
        else:
            await ctx.send("`Unsupported image format, or URL does not end in " + ", ".join(supportedImage) + "`")

    @convert.command()
    async def gif(self, ctx, filelink=None):
        """
        Converts an attached, or linked, image to GIF
        """
        self.check_dir()
        supported = False
        if filelink is None:
            if ctx.message.attachments:
                f = ctx.message.attachments[0]

                for extension in supportedImage:
                    if f.filename.lower().endswith(extension):
                        supported = True
                        r = requests.get(f.url, allow_redirects=True)
                        fileName = "downloads/" + f.filename
            else:
                await ctx.send_help(ctx.command)
                return
        else:
            for extension in supportedImage:
                if filelink.lower().endswith(extension):
                    r = requests.get(filelink, allow_redirects=True)
                    if filelink.find('/'):
                        fileName = "downloads/" + filelink.rsplit('/', 1)[1]
                    supported = True

        if supported:
            start_time = time.time()
            async with ctx.typing():
                outputtext = await ctx.send("`Downloading image...`")
                try:
                    open(fileName, 'wb').write(r.content)
                except Exception:
                    await outputtext.edit(content="`Failed to download image `")
                    return
                await outputtext.edit(content="`Image downloaded...`")
                if not fileName.endswith('.gif'):
                    await outputtext.edit(content="`Converting to GIF...`")
                    newFileName = "senpai_converted_" + fileName + "_.gif"
                    try:
                        proc = Popen(["ffmpeg", "-i", fileName, "-vf", "palettegen", "downloads/palette.png"])
                        proc.wait()
                        proc = Popen(["ffmpeg", "-i", fileName, "-i", "downloads/palette.png", "-filter_complex", "paletteuse", newFileName])
                        proc.wait()
                    except Exception:
                        await outputtext.edit(content="`Failed to convert to GIF`")
                        return
                    await outputtext.edit(content="`Converted to GIF`")
                    await outputtext.edit(content="`Uploading GIF...`")
                    if os.path.getsize(newFileName) < ctx.guild.filesize_limit:
                        await ctx.send(file=discord.File(newFileName), reference=ctx.message)
                        await outputtext.edit(content="`All done! Completed in " + str(round(time.time() - start_time, 2)) + " seconds`")
                    else:
                        await outputtext.edit(content="`Converted GIF is too large! Cannot send GIF.`")
                    os.remove(fileName)
                    os.remove(newFileName)
                    os.remove("downloads/palette.png")
                    return
                else:
                    await outputtext.edit(content="`You asked me to convert a GIF into a ... GIF`")
                    return
        else:
            await ctx.send("`Unsupported image format, or URL does not end in " + ", ".join(supportedImage) + "`")

    @convert.command(aliases=["jpg"])
    async def jpeg(self, ctx, filelink=None):
        """
        Converts an attached, or linked, image to JPEG
        """
        self.check_dir()
        supported = False
        if filelink is None:
            if ctx.message.attachments:
                f = ctx.message.attachments[0]

                for extension in supportedImage:
                    if f.filename.lower().endswith(extension):
                        supported = True
                        r = requests.get(f.url, allow_redirects=True)
                        fileName = "downloads/" + f.filename
            else:
                await ctx.send_help(ctx.command)
                return
        else:
            for extension in supportedImage:
                if filelink.lower().endswith(extension):
                    r = requests.get(filelink, allow_redirects=True)
                    if filelink.find('/'):
                        fileName = "downloads/" + filelink.rsplit('/', 1)[1]
                    supported = True

        if supported:
            start_time = time.time()
            async with ctx.typing():
                outputtext = await ctx.send("`Downloading image...`")
                try:
                    open(fileName, 'wb').write(r.content)
                except Exception:
                    await outputtext.edit(content="`Failed to download image `")
                    return
                await outputtext.edit(content="`Image downloaded...`")
                if not fileName.endswith('.jpeg') and not fileName.endswith('.jpg'):
                    await outputtext.edit(content="`Converting to JPEG...`")
                    newFileName = "senpai_converted_" + fileName + "_.jpeg"
                    err = self.ffmpeg_img(fileName, newFileName, None, None, None)
                    if err == 1:
                        await outputtext.edit(content="`Failed to convert to JPEG`")
                        return
                    await outputtext.edit(content="`Converted to JPEG`")
                    await outputtext.edit(content="`Uploading JPEG...`")
                    await ctx.send(file=discord.File(newFileName), reference=ctx.message)
                    await outputtext.edit(content="`All done! Completed in " + str(round(time.time() - start_time, 2)) + " seconds`")
                    os.remove(fileName)
                    os.remove(newFileName)
                    return
                else:
                    await outputtext.edit(content="`You asked me to convert a JPEG into a ... JPEG`")
                    return
        else:
            await ctx.send("`Unsupported image format, or URL does not end in " + ", ".join(supportedImage) + "`")

    @convert.group()
    async def boxart(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @boxart.command(name="nds", aliases=["dsi"])
    async def ds_boxart(self, ctx, filelink=None):
        """
        Converts an attached, or linked, image to a DS Box Art
        """
        self.check_dir()
        supported = False
        if filelink is None:
            if ctx.message.attachments:
                f = ctx.message.attachments[0]

                for extension in supportedImage:
                    if f.filename.lower().endswith(extension):
                        supported = True
                        r = requests.get(f.url, allow_redirects=True)
                        fileName = "downloads/" + f.filename
            else:
                await ctx.send_help(ctx.command)
                return
        else:
            for extension in supportedImage:
                if filelink.lower().endswith(extension):
                    r = requests.get(filelink, allow_redirects=True)
                    if filelink.find('/'):
                        fileName = "downloads/" + filelink.rsplit('/', 1)[1]
                    supported = True

        if supported:
            start_time = time.time()
            async with ctx.typing():

                outputtext = await ctx.send("`Downloading image...`")
                try:
                    open(fileName, 'wb').write(r.content)
                except Exception:
                    await outputtext.edit(content="`Failed to download image `")
                    return

                await outputtext.edit(content="`Image downloaded...`")
                await outputtext.edit(content="`Converting to PNG...`")
                newFileName = "downloads/senpai_converted_" + fileName[10:] + "_.png"
                err = self.ffmpeg_img(fileName, newFileName, "128:115", None, None)
                if err == 1:
                    await outputtext.edit(content="`Failed to convert to PNG`")
                    return
                await outputtext.edit(content="`Converted to PNG`")
                await outputtext.edit(content="`Uploading boxart...`")
                await ctx.send(file=discord.File(newFileName), reference=ctx.message)
                await outputtext.edit(content="`All done! Completed in " + str(round(time.time() - start_time, 2)) + " seconds`")
                os.remove(fileName)
                os.remove(newFileName)
                return

        else:
            await ctx.send("`Unsupported image format, or URL does not end in " + ", ".join(supportedImage) + "`")

    @boxart.command(name="gba", aliases=["fds", "gbc", "gb"])
    async def gba_boxart(self, ctx, filelink=None):
        """
        Converts an attached, or linked, image to a GB, GBC, GBA or FDS Box Art
        """
        self.check_dir()
        supported = False
        if filelink is None:
            if ctx.message.attachments:
                f = ctx.message.attachments[0]
                for extension in supportedImage:
                    if f.filename.lower().endswith(extension):
                        supported = True
                        r = requests.get(f.url, allow_redirects=True)
                        fileName = "downloads/" + f.filename
            else:
                await ctx.send_help(ctx.command)
                return
        else:
            for extension in supportedImage:
                if filelink.lower().endswith(extension):
                    r = requests.get(filelink, allow_redirects=True)
                    if filelink.find('/'):
                        fileName = "downloads/" + filelink.rsplit('/', 1)[1]
                    supported = True

        if supported:
            start_time = time.time()
            async with ctx.typing():
                outputtext = await ctx.send("`Downloading image...`")
                try:
                    open(fileName, 'wb').write(r.content)
                except Exception:
                    await outputtext.edit(content="`Failed to download image `")
                    return
                await outputtext.edit(content="`Image downloaded...`")
                if not fileName.endswith('.png'):
                    await outputtext.edit(content="`Converting to PNG...`")
                    newFileName = "downloads/senpai_converted_" + fileName[10:] + "_.png"
                    err = self.ffmpeg_img(fileName, newFileName, "115:115", None, None)
                    if err == 1:
                        await outputtext.edit(content="`Failed to convert to PNG`")
                        return
                await outputtext.edit(content="`Uploading boxart...`")
                await ctx.send(file=discord.File(newFileName), reference=ctx.message)
                await outputtext.edit(content="`All done! Completed in " + str(round(time.time() - start_time, 2)) + " seconds`")
                os.remove(fileName)
                os.remove(newFileName)
                return

        else:
            await ctx.send("`Unsupported image format, or URL does not end in " + ", ".join(supportedImage) + "`")

    @boxart.command(name="nes", aliases=["gen", "md", "sfc", "ms", "gg"])
    async def nes_boxart(self, ctx, filelink=None):
        """
        Converts an attached, or linked, image to a NES, Super Famicom, GameGear, Master System, Mega Drive or Genesis Box Art
        """
        self.check_dir()
        supported = False
        if filelink is None:
            if ctx.message.attachments:
                f = ctx.message.attachments[0]
                for extension in supportedImage:
                    if f.filename.lower().endswith(extension):
                        supported = True
                        r = requests.get(f.url, allow_redirects=True)
                        fileName = "downloads/" + f.filename
            else:
                await ctx.send_help(ctx.command)
                return
        else:
            for extension in supportedImage:
                if filelink.lower().endswith(extension):
                    r = requests.get(filelink, allow_redirects=True)
                    if filelink.find('/'):
                        fileName = "downloads/" + filelink.rsplit('/', 1)[1]
                    supported = True
        if supported:
            start_time = time.time()
            async with ctx.typing():
                outputtext = await ctx.send("`Downloading image...`")
                try:
                    open(fileName, 'wb').write(r.content)
                except Exception:
                    await outputtext.edit(content="`Failed to download image `")
                    return
                await outputtext.edit(content="`Image downloaded...`")
                if not fileName.endswith('.png'):
                    await outputtext.edit(content="`Converting to PNG...`")
                    newFileName = "downloads/senpai_converted_" + fileName[10:] + "_.png"
                    err = self.ffmpeg_img(fileName, newFileName, "84:115", None, None)
                    if err == 1:
                        await outputtext.edit(content="`Failed to convert to PNG`")
                        return
                await outputtext.edit(content="`Uploading boxart...`")
                await ctx.send(file=discord.File(newFileName), reference=ctx.message)
                await outputtext.edit(content="`All done! Completed in " + str(round(time.time() - start_time, 2)) + " seconds`")
                os.remove(fileName)
                os.remove(newFileName)
                return
        else:
            await ctx.send("`Unsupported image format, or URL does not end in " + ", ".join(supportedImage) + "`")

    @boxart.command(name="snes")
    async def snes_boxart(self, ctx, filelink=None):
        """
        Converts an attached, or linked, image to an SNES Box Art
        """
        self.check_dir()
        supported = False
        if filelink is None:
            if ctx.message.attachments:
                f = ctx.message.attachments[0]

                for extension in supportedImage:
                    if f.filename.lower().endswith(extension):
                        supported = True
                        r = requests.get(f.url, allow_redirects=True)
                        fileName = "downloads/" + f.filename
            else:
                await ctx.send_help(ctx.command)
                return
        else:
            for extension in supportedImage:
                if filelink.lower().endswith(extension):
                    r = requests.get(filelink, allow_redirects=True)
                    if filelink.find('/'):
                        fileName = "downloads/" + filelink.rsplit('/', 1)[1]
                    supported = True
        if supported:
            start_time = time.time()
            async with ctx.typing():
                outputtext = await ctx.send("`Downloading image...`")
                try:
                    open(fileName, 'wb').write(r.content)
                except Exception:
                    await outputtext.edit(content="`Failed to download image `")
                    return
                await outputtext.edit(content="`Image downloaded...`")
                if not fileName.endswith('.png'):
                    await outputtext.edit(content="`Converting to PNG...`")
                    newFileName = "downloads/senpai_converted_" + fileName[10:] + "_.png"
                    err = self.ffmpeg_img(fileName, newFileName, "158:115", None, None)
                    if err == 1:
                        await outputtext.edit(content="`Failed to convert to PNG`")
                        return
                await outputtext.edit(content="`Uploading boxart...`")
                await ctx.send(file=discord.File(newFileName), reference=ctx.message)
                await outputtext.edit(content="`All done! Completed in " + str(round(time.time() - start_time, 2)) + " seconds`")
                os.remove(fileName)
                os.remove(newFileName)
                return
        else:
            await ctx.send("`Unsupported image format, or URL does not end in " + ", ".join(supportedImage) + "`")

    @convert.command()
    async def dsimenu(self, ctx, filelink=None):
        """
        Converts an attached, or linked, image to a TWLMenu++ DSi Menu Theme
        """
        self.check_dir()
        supported = False
        if filelink is None:
            if ctx.message.attachments:
                f = ctx.message.attachments[0]

                for extension in supportedImage:
                    if f.filename.lower().endswith(extension):
                        supported = True
                        r = requests.get(f.url, allow_redirects=True)
                        fileName = "downloads/" + f.filename
            else:
                await ctx.send_help(ctx.command)
                return
        else:
            for extension in supportedImage:
                if filelink.lower().endswith(extension):
                    r = requests.get(filelink, allow_redirects=True)
                    if filelink.find('/'):
                        fileName = "downloads/" + filelink.rsplit('/', 1)[1]
                    supported = True

        if supported:
            start_time = time.time()
            async with ctx.typing():
                outputtext = await ctx.send("`Downloading image...`")
                try:
                    open(fileName, 'wb').write(r.content)
                except Exception:
                    await outputtext.edit(content="`Failed to download image `")
                    return
                await outputtext.edit(content="`Image downloaded...`")
                if not fileName.endswith('.png'):
                    await outputtext.edit(content="`Converting to PNG...`")
                    newFileName = "senpai_converted_" + fileName + "_.png"
                    err = self.ffmpeg_img(fileName, newFileName, "208:156", None, None)
                    if err == 1:
                        await outputtext.edit(content="`Failed to convert to PNG`")
                        return
                await outputtext.edit(content="`Uploading DSi Menu image...`")
                await ctx.send(file=discord.File(newFileName), reference=ctx.message)
                await outputtext.edit(content="`All done! Completed in " + str(round(time.time() - start_time, 2)) + " seconds`")
                os.remove(fileName)
                os.remove(newFileName)
                return
        else:
            await ctx.send("`Unsupported image format, or URL does not end in " + ", ".join(supportedImage) + "`")

    @convert.command()
    async def dsmp4(self, ctx, filelink=None):
        """
        Converts an attached, or linked, video to a MPEG4 Player for DSi Video
        """
        self.check_dir()
        supported = False
        if filelink is None:
            if ctx.message.attachments:
                f = ctx.message.attachments[0]

                for extension in supportedImage:
                    if f.filename.lower().endswith(extension):
                        supported = True
                        r = requests.get(f.url, allow_redirects=True)
                        fileName = "downloads/" + f.filename
            else:
                await ctx.send_help(ctx.command)
                return
        else:
            for extension in supportedImage:
                if filelink.lower().endswith(extension):
                    r = requests.get(filelink, allow_redirects=True)
                    if filelink.find('/'):
                        fileName = "downloads/" + filelink.rsplit('/', 1)[1]
                    supported = True
        if supported:
            async with ctx.typing():
                start_time = time.time()
                size_large = False
                outputtext = await ctx.send("`Downloading video...`")
                print(outputtext)
                try:
                    open(fileName, 'wb').write(r.content)
                except Exception:
                    await outputtext.edit(content="`Failed to download video`")
                    return
                await outputtext.edit(content="`Converting video...`")
                with open(os.devnull, "w") as devnull:
                    subprocess.run(['ffmpeg', '-i', fileName, '-f', 'mp4', '-vf', "fps=24000/1001, colorspace=space=ycgco:primaries=bt709:trc=bt709:range=pc:iprimaries=bt709:iall=bt709, scale=256:144", '-dst_range', "1", '-color_range', "2", '-vcodec', 'mpeg4', '-profile:v', "0", '-level', "8", "-q:v", "2", "-maxrate", "500k", "-acodec", "aac", "-ar", "32k", "-b:a", "64000", "-ac", "1", "-slices", "1", "-g", "50", 'downloads/senpai_converted.mp4'], stdout=devnull)
                if os.path.getsize("downloads/senpai_converted.mp4") < ctx.guild.filesize_limit:
                    await ctx.send(file=discord.File("downloads/senpai_converted.mp4"), reference=ctx.message)
                else:
                    size_large = True
                    await outputtext.edit(content="`Converted video is too large! Cannot send video.`")
                os.remove("downloads/senpai_converted.mp4")
                os.remove(fileName)
                if not size_large:
                    await outputtext.edit(content="`Done! Completed in " + str(round(time.time() - start_time, 2)) + " seconds`")
        else:
            return

    @convert.command(aliases=["mp4"])
    async def video(self, ctx, filelink=None):
        """
        Converts an attached, or linked, video to MP4
        """
        self.check_dir()
        supported = False
        if filelink is None:
            if ctx.message.attachments:
                f = ctx.message.attachments[0]

                for extension in supportedImage:
                    if f.filename.lower().endswith(extension):
                        supported = True
                        r = requests.get(f.url, allow_redirects=True)
                        fileName = "downloads/" + f.filename
            else:
                await ctx.send_help(ctx.command)
                return
        else:
            for extension in supportedImage:
                if filelink.lower().endswith(extension):
                    r = requests.get(filelink, allow_redirects=True)
                    if filelink.find('/'):
                        fileName = "downloads/" + filelink.rsplit('/', 1)[1]
                    supported = True
        if supported:

            async with ctx.typing():
                start_time = time.time()
                size_large = False
                outputtext = await ctx.send("`Downloading video...`")
                print(outputtext)
                try:
                    open(fileName, 'wb').write(r.content)
                except Exception:
                    await outputtext.edit(content="`Failed to download video`")
                    return
                await outputtext.edit(content="`Converting video...`")
                with open(os.devnull, "w") as devnull:
                    subprocess.run(["ffmpeg", "-y", "-an", "-i", fileName, "-vcodec", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "baseline", "-level", "3", "-s", "852x480", '-vf', "scale=640:trunc(ow/a/2)*2", "downloads/senpai_converted.mp4"], stdout=devnull)

                await outputtext.edit(content="`Uploading Video...`")
                if os.path.getsize("downloads/senpai_converted.mp4") < ctx.guild.filesize_limit:
                    await ctx.send(file=discord.File("downloads/senpai_converted.mp4"), reference=ctx.message)
                else:
                    size_large = True
                    await outputtext.edit(content="`Converted video is too large! Cannot send video.`")
                os.remove("downloads/senpai_converted.mp4")
                os.remove(fileName)
                if not size_large:
                    await outputtext.edit(content="`Done! Completed in " + str(round(time.time() - start_time, 2)) + " seconds`")
        else:
            return


def setup(bot):
    bot.add_cog(Convert(bot))
