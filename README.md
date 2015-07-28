# SMBC RSS Plus Feed

*Also known as the SMBC + Red Button or Bonus Image Feed*

![](readme/button.jpg)

I have a question to ask you!

Do you use a mobile RSS Reader? How many of them have added support for showing the contents of `alt` when you long-press on an image? I'm guessing we have to thank the popularity of XKCD for that!

Unfortunately, the red-button bonus image situation with SMBC is a bit more complicated than that. It is *usually* at some URL that is derived from the original image. Also, SMBC is probably not as popular as XKCD to get special functionality developed for it.

To address this, many people created their own Yahoo Pipes to solve this. I've since forked one of these to address issues with the new "post-png" button images. Alas, Yahoo Pipes is shutting down. As such, this whole operation is going to need a new implementation. This is it.

## Rough New Architecture

It's just a Heroku app that has no dynos and the Heroku scheduler addon running a script every 10 minutes. Still free, still constantly available. Uses S3 to serve and for persistence. KISS, never worry. When *their* free lunch runs out (and it already has for 24/7 HTTP serving web apps), I can move it.

As it stands, S3 will probably cost me about 2 and a few more cents a month to host. It's a small cost. But, IDGAF, and that's the spirit of it all.

### TODO

* As this is no longer limited to regular expressions, perhaps we could scrape the linked comic's page for the *exact* red button link. A broken image comes by every once in a while but maybe the complexity just isn't worth it?

## RIP Yahoo Pipes

This was originally based on this Yahoo Pipe. I can't link it because Yahoo Pipes is going to be dead but I can provide this screenshot of the pipe and the two cut-off text-fields. I've also left a JSON dump of the *SHUTDOWN-IMMINENT!* version under the `pipes_archive` directory. Unfortunately, I don't know who I forked my pipe from.

This was the whole pipe:

![](readme/original_pipe.png)

Screenshot:

* Replace: `<img src="http://www\.smbc-comics\.com/comics/(\d+\-\d+)\.([pg][ni][gf])"/>(.*)`
* With: `<img src="http://www\.smbc-comics\.com/comics/$1\.$2"><br><br><img src="http://www\.smbc-comics\.com/comics/$1after\.png">$3`

That was the whole thing!

That said, as I'm writing this before Yahoo Pipes shuts down forever, there's like 10 or 20 variants of this pipe on Yahoo Pipes and they're all pretty similar.
