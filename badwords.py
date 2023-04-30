import spacy
from profanity_filter import ProfanityFilter

cense = spacy.load('en_core_web_sm')
pf = ProfanityFilter(nlps={'en':cense})
cense.add_pipe(pf.spacy_component, last=True)

def bad_words_highlight(text):

    noBad = True
    replaced = []

    for token in cense(text):
        isBad = token._.is_profane

        if isBad == True:
            noBad = False

            if str(token) not in replaced:
                replaced.append(str(token))
                text = text.replace(str(token),"<span class=\"highlighter\">"+str(token)+"</span>")

    return {'isBad':not noBad,'rtext':text} 


if __name__ == "__main__":

    print(bad_words_highlight("you are a shirt shirt"))