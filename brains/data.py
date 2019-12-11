# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

import time

DATA = {
    1: [
        # found
        "No Grandfather, no Father; no Father, no Tim; no Tim, no killing.",
        "Snow falls and is white; the falling is a process, the whiteness is not.",     # ^ ^ - - ^; - ^ - - - ^ -; - ^ - - ^
        "We sometimes say: in later life I will be a different person.",
        "The game, one would like to say, has not only rules but also a point.",
        "Suppose that I cling to some rock as a mere means of escaping death.",
        "One of my strongest desires is that Venice never be destroyed.",
        "My mother did have many months of suffering, but she is now dead.",
        "One of my strongest desires was to be a successful parent.",
        "What does it mean to stop when the marks of going on are no longer?",
        "Suppose, as I stare at a glass in front of me, I say or think: There.",
        "Why is science so rare and faith so common in human history?",
        "We are not simply fallible at the margins but broadly inept.",                 # - - ^ ^ -; ^ - - - - ^ -; - ^ - - ^
        "How can man, who is born free, rightly come to be everywhere in chains?",
        "When I turn my eye inward, I find nothing but doubt and ignorance.",
        "You have an auto accident one winter night on a lonely road.",
        "What matters for now is not how we begin, but how we continue.",
        "Who can be loyal to a God who cannot be asked for anything?",
        "You may undersell a competitor, but you must not murder him.",
        "A proposition contains the form, but not the content, of its sense.",
        "Look at the blue of the sky and say to yourself How blue the sky is!",
        "I am not used to measuring temperatures on the Fahrenheit scale.",
        "Fear for others is only a shade better than fear for ourselves.",
        "Why was the world not created sooner? Because there was no sooner.",
        "How many facts or propositions are conveyed by a photograph?",
        "We often succumb to temptation with calm and even with finesse.",

        # real haikus (not necessarily 5-7-5)
        "An old silent pond. A frog jumps into the pond — Splash! Silence again.",      # - ^ ^ - ^; - ^ ^ - - - ^; ^ ^ - - ^
        "A world of dew, And within every dewdrop A world of struggle.",                # - ^ - ^; - - ^ ^ - ^ -; - ^ - ^ -
        "The light of a candle Is transferred to another candle — Spring twilight",
        "Over the wintry Forest, winds howl in rage With no leaves to blow.",
        "The apparition of these faces in the crowd; Petals on a wet, black bough.",    # - - - ^ - - - ^ - - - ^; ^ - - - ^ ^ ^
        "The taste Of rain — Why kneel?",
        "love between us is speech and breath. loving you is a long river running.",
        "The west wind whispered, And touched the eyelids of spring: Her eyes, Primroses.",
        "Whitecaps on the bay: A broken signboard banging In the April wind.",
        "an aging willow — its image unsteady in the flowing stream",
        "Snow in my shoe Abandoned Sparrow's nest",
        "this piercing cold – in the bedroom, I have stepped on my dead wife's comb",
        "the Flower Festival – a mother’s womb is only for temporary lodging",
        "sound of dance music — the last fishing boat throbs into place",
        "shipping oars I hold my breath to hear snow on the water",
        "after the crash the doll’s eyes jammed open",
        "midday heat soldiers on both sides roll up their sleeves",
        "cold night the dashboard lights of another car",
        "dune wind — the blackened seed pods of a bush lupine",
        "On a branch floating downriver a cricket, singing.",
        "As cool as the pale wet leaves of lily-of-the-valley She lay beside me in the dawn.",
        "Lightning shatters the darkness ― the night heron's shriek.",
        "A freezing morning: I left a bit of my skin on the broomstick",
        "I write, erase, rewrite, Erase again, and then A poppy blooms",
        "fallen leaves the abbot sweeps around them",
        "losing its name a river enters the sea",
        "Moon's brightness I wonder where they're bombing",
        "First snow Falling On the half-finished bridge.",
        "See the river flow In a long unbroken line On the field of snow.",
        "Sudden spring storm-a family of ducks paddles around the deserted lake.",
        "The summer river: although there is a bridge, my horse goes through the water.",
        "Sick on a journey-Over parched fields Dreams wander on.",
    ],
    0: [

        # found
        "Further constraints could be added, but they will not be considered here.",    # ^ - - ^ - - ^ -; - - - ^ - - ^ - -
        "Also, some special flexibility in the theory is discussed.",
        "Similarly, of course, for my stepping back from my preferences.",
        "After all, there is nothing indeterminate about such cases.",
        "Its premises claim the least, and are therefore the hardest to deny.",
        "The evidence gives little support to any of these suggestions.",
        "I will return to this matter when it becomes relevant later.",
        "What should worry us about the ideal objects is the following.",
        "In neither case is synonymy to be claimed for the paraphrase.",
        "In neither case does the sentence refer to a generic action.",
        "But there are plenty of other contexts in which the same need presses.",
        "But these events do not sound like ordinary bodily movements.",
        "We can, however, take it as given that most beliefs are correct.",
        "This reply does not, as might first be thought, merely restate the problem.",
        "But then there is a question how we understand the metalanguage.",
        "Our problem is that they have altogether too much in common.",
        "Even with working models there are limits to isomorphism.",
        "The last phrase, I have been suggesting, contains an ambiguity.",
        "Here too, I think it is clear that the evidence supports my account.",
        "Why are the authors of these theories not impressed by these examples?",
        "There are several such puzzling examples in the literature.",
        "Such costs would not be lightly recouped, one would think. These are good questions.",
        "The second concept which is in question is that of necessity.",
        "But even when they are unhappy, I do not think that they are bored.",
        "In his next chapter, he maintains the same thesis as regards number.",
        "In each there are two kinds, one immediate and one derivative.",
        "This seems to show that we must distinguish between content and object.",
        "More complicated propositions can be dealt with on the same lines.",
        "At best, such a claim is controversial, at worst, obviously false.",
        "Moreover, it is plausible that sometimes they ought to come apart.",
        "For some discussion of dispositions, see a few paragraphs hence.",
        "With this in mind, let us turn to the second stage of their argument.",
        "We present them here, and discuss some related conceptions of set.",
        "See the entry on the interpretation of probability.",
        "More recent studies have demonstrated that things are much more complex.",
        "Several problems with this program make themselves felt immediately.",
        "Therefore they are not eligible to stand in causal dependence.",
        "But if this is a case of piecemeal causation, we have no problem.",
        "These verbs take clauses rather than direct objects as their complements.",
        "Those assumptions are controversial, but I need not defend them here.",
        "The limits discussed in this chapter are far more prosaic than those.",
        "Endless examples can be constructed to the foregoing pattern.",
        "Examples of this type can be constructed for the other senses.",
        "Rather, it connects absolute and relative justification.",
        "Nevertheless, I want to proceed on a less adventurous track.",
        "Nevertheless, this is an important part of objectivity.",
        "Otherwise it is not freedom that I display but weakness of will.",
        "While this seems to me true, there is a natural way to dispute it.",
        "Rather it depends on the truth about ethics. What I think is this.",
        "Rational agents make things happen, that is, they are efficacious.",
        "The distribution of opportunities is also important.",
        "In addition to her studies, she devoted time to writing plays.",
        "Therefore, He knows the entirety of that which He has determined.",
        "He later became a member of the right wing Hegelian school.",
        "That traditional view dominated mainstream readings of the text.",
        "Eventually, he needed people like his wife to read to him.",
        "A molecular fact f is a conjunction of atomic facts.",
        "Is not one of these partitions privileged by the grounding relation?",
        "However, there is a deeper result here which we discuss below.",
        "Thus, the class of all cardinals is not a set, but a proper class.",
        "Matthew Clayton and Richard Arneson press this complaint against Rawls.",
        "The analogy with grammar might seem to break down at just this point.",
        "To understand this distinction, consider the following cases.",
        "There are many ways in which one can attempt to block the argument.", 
        "The real issue, to reiterate the point, is one of relevance.",
        "The above list is not meant to be exhaustive or especially clean.",
        "Interested readers may listen to two sound clips of Russell speaking.",
        "A fourth volume on geometry was planned but never completed.",
        "APPENDIX B Some More Questions About Science [For context, see p.",
        "Consequently, the above so-called law is not a law of nature.",
        "From this primitive conjunction follow many important results.",
        "To do this, we need a bridge between the abstract and concrete domains.",
    ],
}

TEST_SOURCES = {
    1: [
    ],
    0: [
    ],
}

def get():
    data = []
    target = []
    t1 = time.time()
    for cls, texts in DATA.iteritems():
        for text in texts:
            data.append(text)
            target.append(cls)
    return data, target
