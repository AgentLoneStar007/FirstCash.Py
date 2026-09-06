# Disclaimer

This API was not meant to be public. I found documentation for it purely by accident when trying to understand why I
couldn't click on the "Store Details" button on an item on their website. I built this library for two reasons:
1) For a learning exercise. (I've never built a Python library.)
2) In the hopes that someone may find it useful.

I took every precaution I could to avoid harming (think: rate-limits, sending malformed data, exposing endpoints that
actually create data, etc.) their systems, and I'd greatly appreciate it if you did the same. Please consider good
practices when creating an application using this library: 
- Cache your data.
- Avoid sending too many requests.
- Use the mobile app to acquire your API key rather than digging through the source code of official websites. This 
shouldn't be too difficult since the key is present in the URL.

**And most importantly,** remember that if FirstCash sends you a request to take down your application, you need to
comply. If this library randomly goes missing one day, that's why. This is their system, not yours or mine.

# FirstCash System Notes

FirstCash uses a system called V2 for their pawn management, point-of-sale system, and other services. This system
(from what I can tell) is in no way related to this API. Either V2 manages the inventory and this API pull from it,
or the inventory is kept in a separate database and they both pull from it. Regardless, this API does have some minor
discrepancies between V2; namely, categories are more fine-tuned in V2 than what is offered when pulling from the
`fetchCategories()` method's endpoint. I also believe the codes may be different in places, but I wouldn't swear to
this. A lot of this I'm pulling from memory because I used to work there a long time ago.

Regardless, some documentation may simply have to be built up over time via usage of the API, rather than pulling from
documentation here or elsewhere. This API is not meant to have public access.

# Query and Data Storage Notes

FirstCash's inventory is added to and edited by employees. Not everyone understands the importance of consistent data
entry, and FirstCash does not have the need to enforce consistency. In other words, sometimes you'll find a product
with a serial number in place of the model number, or a manufacturer of "computer," or some other thing like that. The
best example I have off the top of my head is the Meta Quest 2. At the shop I worked at, many people couldn't agree
on how to list those in our system, which resulted in two identical Quests sitting on the shelf, one being marked for
\$80 and the other for \$120, simply because someone used Facebook as the manufacturer, causing the system to recommend
an incorrect price.

What I'm saying in a nutshell is that data validation is best done on your side. If you come across a game console with
a manufacturer of Oculus or Facebook, or a model number of Quest 2, it's best to list that in your own database as a
game console with a manufacturer of Meta and a model number of "KW49CM."

**Note:** Just because this may be the case of how data is stored, this is not an excuse to walk into your local pawn
shop and get mad. Rather, barter the price. This is the beauty of a pawn shop. If you find some hidden treasure, you
can try to haggle the price lower or higher. Give your reasoning. Explain why you think the price is incorrect. And
you just might get lucky!
