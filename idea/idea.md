# Emoji-site

This is going to be a quality weeb site where users can easily find high quality, well categorized, images.
Each image has to have certain quality to it, we don't want spam and ugly/low quality images.
They also have to be easily sortable/searchable and easy to find, thus each image has to be correctly categorized.
For this we need an extremely good categorizing and tag system, for this we need it to satisfy main 2 parts:
website and API.

When in website it is beneficial to find subcategory you want trough few clicks, instead of categories being all
over the place and you having problems finding what you want. Point is few clicks are fine, but for API my idea is to
simply enter word or two and it will fetch the closest image for that that it can find.

## Website Categories
Here is the current idea for website categorization:

"""
Anime -> Title
      -> Character

Game -> Title
     -> Character
""

Above example would cover the vast majority of weeb images, for example let's have Marisa from Touhou - she would then 
be in all 4 subcategories. More specifically she would be in:

"""
Anime -> Title -> Touhou
      -> Character -> Marisa

Game -> Title -> Touhou
     -> Character -> Marisa
"""

And if you think about it, it might be beneficial to go even lower due to Touhou having certain popular
sub-franshizes, like KKHTA. So you might think that this would be even better:

"""
Anime -> Title -> Touhou -> KKHTA
      -> Character -> Marisa

Game -> Title -> Touhou -> KKHTA
     -> Character -> Marisa
"""

I am still not sure if I will this way, or maybe include it in tag.
Problem with that way is that we might not now all of the sub-franshizes of our images, making categorization difficult.

## API

Tags will be used primarily for API search.
For example if someone searches for "marisa happy animated" we would fetch the first animated Marisa image where she is
happy. Alternative would be to use categories and send querry that would specifically target specific category but that
is extra work when in most cases API users would just need a quick reaction image.

My idea is to have the API as some sort of alternative for Discord emojies.
Due to Discord emoji limit size and due to you needing to have nitro to use them in other servers I would like for this
API to be a quick alternative for users to use for their reaction images.


## Tags

I have no idea how to do this, as just adding random tags will end up them being all over the place.
I need some sort of categorization for tags as well.
For example I want each emoji to be tagged for: actions, expressions, how many character are there etc

Specific example #1:
Let us image an emoji with Anya (Spy X Family) is jumping while being happy.
This would have action of jump and expressions of happy.
Additional problems are synonyms for words, for the above example with API search of "anya jump happy" users could also
search "anya jumping happy" so we need to probably add synonyms for each word to satisfy what the users might search for.


Specific example #2:
Nue (Touhou) wearing 3d glasses, eating (implied popcorn) and implied she is watching a movie.
This case becomes a bit more difficult:
- expression -> I don't think there is one, could be relaxed or satisfied, but I don't think those matter.
- action -> watching
         -> eating
We are also missing representation that she is wearing 3d glasses, and our actions lack context information
for movie and popcorn.

So we could use 2 word for those like "watching movie" or "eating popcorn" but then we would have to have that for each
action like "watching sunrise" or "eating burger" and for each we would have to have synonym like "watch movie"
and "watch sunrise" and problem being duplication.

Maybe we could to some sort of hierachy where we would have

watch -> movie
      -> sunrise

And then each of those objects could have relation to possible synonims.
How the hell would that work with SQL search tho :/

Maybe I should simply replace -ing word with their non-ing word, so if user searched "anya jumping happy" it would
get converted to "anya jump happy" but english is meesed up and I'm sure there would be a ton of exceptions, not to
mention other word transformations like "happily"

Current SQL idea is to maybe search each word separately? Like first I search for first word and all of it's synonims,
so I would get all anya tagged emojies, then next word and next.

Additional question is do I even need tags? Anya will clearly be in character category so I can just search that.
And these expressions and actions will be specific tags.

## Visual preview
Current idea, visual preview of emoji page.

### Top section
"""
                ┌─────────────────┐
                │    EMOJI        │
                │    IMAGE        │
                │                 │
                │                 │
                │                 │
                │                 │
                └─────────────────┘
  X likes  X bookmarks  X collectionS  x downloads
"""
X represents icon: hearth for likes, bookmark for bookmarks, plus for collections, arrow down for downloads
Text is replaced by actual count.
Note: Since I can not controll downloads on website, mabye "views" is betters (with eye icon), so basically each
time emoji is opened in webpage, or is querried with API we add +1 count
Maybe separate those stats to 2 fields?
Add stats? Like monthly, by user etc

### Bottom section

#### Categories
It gets complicated to display a tree, so for now just display all categories raw

"""
------------------------------------------------------------------------------------------------------------------------
Anime -> Title -> Touhou
Anime -> Character -> Marisa
Game -> Title -> Touhou
Game -> Character -> Marisa
------------------------------------------------------------------------------------------------------------------------
"""
I do not like that there are so many lines, and there could be even more.
Note: Title CAN NOT belong to Anime and Game at the same time! As it is "main" category.
This would cause problems when trying to discern the two.

After many options just use the above example, and if you use tree use it on above example.
You cannot combine subcategories since they are not tied to the same parents.

Additionally I think each category should have a "full name" field that will discern it when you are viewing it's page.
For example if you click on title in  Anime -> Title you will be brought to category page just saying
"Title" and you will have no context for what the title stands for. So either show it's parent or use the full name.

For example for Anime we could use Aime series, same with game.
But then what about possible nested subcategories? Scrach that, on category page just show the tree for it.



# Stats

We need view stats, that will be anonymized.
We need it per day, then we can sort/filter by week/month/year

Users can also have their own stats, but that requires them using API and consenting to stats.
It would pretty much be the same as global stats, but the model would inherit from it and have additional field
for user.


# API security

API Key etc

# User profile for api keys

Integrate Discord or gmail oauth

# CDN

Integrate some CDN to serve images, django is only for fetching URLs.

We absolutely need NO loss in quality.

# DNS / DDos protection

Fascade behind cloudflare or some other provider.


For category hierarchy we would simply go from current category to all of the parent categories and construct a tree.
Due to some subcategories possibly belonging to 2 or more different parent categories, the tree would look as above.


Each category can be marked as "main" (or similar). This means that it can have subcategories but objects cannot be tied
to them. For example if we have Yui from K-ON! emoji we would have hierarchy like this:

Anime -> Character -> Yui
Anime -> Title -> K-ON!

In these cases our object is tied to "Yui" and "K-ON!" but cannot be directly tied to Anime/Character/Title
Those are only there for further, more broad, filtering.
For example in webpage we can select main category Anime, and then select "Filter by" either character or title

Question: How many nesting can there be? What if we have case like:

main -> main -> secondary -> main
             -> secondary



# DESCRIBE IMAGES

character: koishi
expression: happy
state: bald, big, tall, fit, beautiful
action: jump
object: knife
place: mental assylum

Pretty sure the above would work on vast majority of images, including reaction images.
Some words like cute are not an expression, but a "positive descriptive adjective" with "positive" being just the name,
it can also be "ugly". So for those I'm not sure what to call them except that "official" term, but
that is a slippery sloper as I could then use an "official" word for everything and make it more complex.
Maybe "state" would be better, all of PDA like big, tall, fit, beautiful, cute could go in it?
Some word that are missing: bald, could also be a state?


# SPACY auto pipenv install file and add to pipenv
pipenv install $(spacy info en_core_web_trf --url)
