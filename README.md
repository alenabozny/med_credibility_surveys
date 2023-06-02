This is the web application written in Python Flask by:
- Aleksandra Nabożny
- Kamil Warpechowski

Designed by:
- Aleksandra Nabożny

It serves to collect credibility labels for a given samples of medical texts (three consecutive sentences with topical keywords).
Application accepts full article texts + keywords in a JSON format, divide them by samples (sentence triples), and let the administrator to assign evaluation tasks for a given sample to the annotator (Annotators have to get the accounts created first). The application served for the experiments held in 2019-2021 on Polish-Japaneese Academy of Information Technology.

# med_credibility_surveys

## Dane do logowania

login: test
haslo: test


## TODO
REVIEW
 * [ ] tabela Review + powiązania z użytkownikiem i taskiem
 * [ ] rola użytkownika is_reviewer
 * [ ] widok dodawania nowego Review
 * [ ] dodać 'category' do Article
