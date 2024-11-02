naver_lists = ["frustrated", "confused", "determined", "overwhelmed", "impatient", "practical", "sarcastic", "accusatory", "defensive", "conciliatory", "suspicious", "grateful", "concerned", "bitter", "reassuring", "angry", "helpful", "accusing", "apologetic", "dismissive", "inquiring", "shocked", "accusatory", "dismissive", "disappointed", "apologetic", "defensive", "demanding", "exasperated", "reminding", "reluctant", "insistent", "frustrated", "displeased", "irritated", "defensive", "silent", "passionate", "suspicious", "frustrated", "sarcastic", "adamant", "dismissive", "protective", "indignant", "self-loathing", "confused", "regretful", "dismissive", "guilty", "assertive", "insecure", "affectionate", "indifferent", "teasing", "hopeful", "suggestive", "practical", "concerned", "protective", "guilty", "reassuring", "insistent", "resistant", "firm", "confused", "affectionate", "irritated", "perplexed", "blunt", "pragmatic", "captivated", "matter-of-fact", "suggestive", "worried", "surprised", "guilty", "reassuring", "explaining", "concerned", "embarrassed", "exasperated", "defensive", "commanding", "tired", "concerned", "downplaying", "frustrated", "apologetic", "incredulous", "resigned", "warning", "self-deprecating", "distraught", "surprised", "anguished", "casual", "indifferent", "practical", "dismissive", "relieved", "puzzled", "thoughtful", "unenthusiastic", "encouraging", "reluctant", "impatient", "protesting", "flirtatious", "annoyed", "concerned", "embarrassed", "determined", "overwhelmed", "justifying", "exasperated", "insistent", "critical", "disappointed", "assertive", "inquisitive", "admitting", "eager", "resistant", "admiring", "pleased", "teasing", "warning", "complimentary", "accusatory", "disheartened", "uncomfortable", "bitter", "alarmed", "possessive"]

def del_redun(lists):
    new_lists = []
    for i in lists:
        if i not in new_lists:
            new_lists.append(i)
        else:
            print(i)
    return new_lists

print(del_redun(naver_lists))