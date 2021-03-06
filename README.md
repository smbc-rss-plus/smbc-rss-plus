# SMBC RSS Plus Feed

*Also known as the SMBC + Red Button or Bonus Image or Bonus Panel Feed*

![](readme/button.jpg)

I have a question to ask you!

Do you use a mobile RSS Reader? How many of them have added support for showing the contents of `alt` when you long-press on an image? I'm guessing we have to thank the popularity of XKCD for that!

Unfortunately, the red-button bonus image situation with SMBC is a bit more complicated than that. It was previously at some URL that is derived from the original image, but this is no longer guaranteed. Also, SMBC is probably not as popular as XKCD to get special functionality developed for it by major feed reader vendors.

To address this, many people had created their own Yahoo Pipes to solve this. I had forked one of these to address issues with the new "post-png" button images. Alas, Yahoo Pipes had shut down. As such, this whole operation needed a new implementation. This is it.

As mentioned, due to some site changes and some further site changes, the URL of the red button images are no longer guaranteed to line up with the URL for the image. As such, the only thing to do is to scrape the linked comic itself and append an image to the end of the RSS feed. This new architecture is capable of doing that.

## Rough New Architecture

This is a Heroku app that has no dynos and the Heroku scheduler addon running a script every 10 minutes. Still free, still constantly available. Uses S3 to serve and for persistence. KISS, never worry. When *their* free lunch runs out (and it already has for 24/7 HTTP serving web apps), I can move it.
 
With the red button images aligning to the comic image URL less and less, this script was updated to use a Redis instance for caching the results of scraping the comic's HTML. It too is also hosted for free by Heroku for no cost. 

As it stands, S3 will probably cost me about 2 and a few more cents a month to host. It's a small cost. But, IDGAF, and that's the spirit of it all.

## RIP Yahoo Pipes ⚰️

This was originally based on this Yahoo Pipe. It can't be linked because Yahoo Pipes is dead but I can provide this screenshot of the pipe and the two cut-off text-fields. I've also left a JSON dump of the *SHUTDOWN-IMMINENT!* version under the `pipes_archive` directory. Unfortunately, I don't know who I forked my pipe from or who the original author is.

This was the whole pipe:

![](readme/original_pipe.png)

Screenshot:

* Replace: `<img src="http://www\.smbc-comics\.com/comics/(\d+\-\d+)\.([pg][ni][gf])"/>(.*)`
* With: `<img src="http://www\.smbc-comics\.com/comics/$1\.$2"><br><br><img src="http://www\.smbc-comics\.com/comics/$1after\.png">$3`

That was the whole thing!
