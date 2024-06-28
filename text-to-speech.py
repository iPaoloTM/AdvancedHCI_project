from openai import OpenAI
#import the library
from playsound import playsound

text1 = '''C'era una volta, in un piccolo paese circondato da colline verdi e fiori in fiore nel Trentino, un cucciolo di nome Letizia. Era una pallina di pelo soffice con grandi occhi rotondi che brillavano come stelle. Ma, nonostante il suo aspetto adorabile, Letizia non era il cucciolo dolce che ci si potrebbe aspettare. Era sempre arrabbiata e scontrosa, ringhiando a chiunque si avvicinasse e abbaiando per il minimo motivo.

La padrona di Letizia, la signora Serena, era una gentile vecchietta che l'amava moltissimo. Spesso le diceva: "Letizia, mia cara, hai così tanto potenziale per essere felice. Perché sei così arrabbiata?" Ma Letizia sbuffava e si girava dall'altra parte, troppo avvolta nel suo mondo di malumore per ascoltare.

Un giorno, la signora ### La Storia di Letizia: Un Viaggio dalla Rabbia alla Gratitudine

C'era una volta, in un piccolo paese circondato da colline verdi e fiori in fiore nel Trentino, un cucciolo di nome Letizia. Era una pallina di pelo soffice con grandi occhi rotondi che brillavano come stelle. Ma, nonostante il suo aspetto adorabile, Letizia non era il cucciolo dolce che ci si potrebbe aspettare. Era sempre arrabbiata e scontrosa, ringhiando a chiunque si avvicinasse e abbaiando per il minimo motivo.

La padrona di Letizia, la signora Serena, era una gentile vecchietta che l'amava moltissimo. Spesso le diceva: "Letizia, mia cara, hai così tanto potenziale per essere felice. Perché sei così arrabbiata?" Ma Letizia sbuffava e si girava dall'altra parte, troppo avvolta nel suo mondo di malumore per ascoltare.

Un giorno, la signora Serena decise di portare Letizia in un'avventura nella foresta vicina. Sperava che un cambiamento di scenario potesse rallegrarla. Mentre camminavano attraverso la foresta, Letizia continuava a brontolare, senza notare gli uccellini che cantavano o i fiori vibranti che ondeggiavano nella brezza. All'improvviso, uno scoiattolo attraversò il loro cammino, facendo abbiare furiosamente Letizia che iniziò a inseguirlo. Corse e corse, addentrandosi sempre più nella foresta, fino a rendersi conto di essersi persa.

Spaventata, Letizia abbaiò e ululò, ma non ci fu nessuna risposta. Vagò per la foresta, la sua rabbia si trasformò in paura mentre il sole iniziava a tramontare. Proprio quando stava per perdere la speranza, inciampò in una piccola capanna diroccata. Disperata in cerca di aiuto, si avvicinò cautamente.

All'interno della capanna viveva un vecchio eremita di nome Gregorio. Era un uomo saggio che aveva scelto una vita di solitudine per connettersi con la natura e trovare la pace interiore. Quando vide Letizia, la accolse calorosamente, offrendole cibo e riparo. Letizia, sebbene ancora diffidente, accettò la sua gentilezza.

Nei giorni successivi, Gregorio e Letizia divennero amici improbabili. Gregorio aveva un dono con gli animali e con pazienza insegnò a Letizia la bellezza della foresta e l'importanza della pace interiore. Le raccontò storie delle sue stesse difficoltà e di come aveva imparato a trovare gioia nelle piccole cose.

Una storia in particolare colpì profondamente Letizia. Gregorio raccontò di un tempo in cui era stato un giovane uomo, pieno di rabbia e risentimento. Aveva incolpato il mondo per le sue disgrazie fino a quando un giorno incontrò un vecchio viaggiatore che gli impartì una lezione profonda. Il viaggiatore disse: "La felicità non è qualcosa che trovi; è qualcosa che crei. Inizia da dentro."

Ispirata dalla storia di Gregorio, Letizia iniziò a vedere il mondo sotto una luce diversa. Cominciò ad apprezzare la bellezza della foresta e la gentilezza del suo nuovo amico. Piano piano, la sua rabbia iniziò a svanire, sostituita da un senso di gratitudine.


'''

text2 = '''Una mattina, Letizia si svegliò trovando Gregorio intento a preparare una piccola borsa. "È ora che tu torni a casa, Letizia," disse dolcemente. "Hai imparato molto, e la signora Serena deve essere preoccupata per te."

Letizia sentì una fitta di tristezza all'idea di lasciare Gregorio, ma sapeva che aveva ragione. Con il cuore pesante, lo salutò e iniziò il suo viaggio di ritorno a casa. Mentre attraversava la foresta, non poteva fare a meno di notare quanto tutto sembrasse diverso. Gli alberi sembravano più verdi, i fiori avevano un profumo più dolce e persino i canti degli uccelli sembravano più melodiosi.

Quando Letizia finalmente uscì dalla foresta, vide la signora Serena che la aspettava ansiosamente. Vedendo Letizia, il volto della signora Serena si illuminò di gioia. "Oh, Letizia! Ero così preoccupata per te!" esclamò, abbracciandola strettamente.

Con sorpresa della signora Serena, Letizia rispose scodinzolando e facendo una carezza gentile. Non era più il cucciolo arrabbiato e scontroso che era stato prima. Letizia aveva imparato a trovare la felicità e la gratitudine nel suo cuore.

Da quel giorno in poi, la vita di Letizia cambiò in meglio. Divenne conosciuta come il cane più dolce e amorevole del paese. Fece amicizia con gli altri animali, giocò felicemente con i bambini e aiutò persino la signora Serena nel suo giardino.

Il viaggio di Letizia le aveva insegnato una lezione inestimabile: la vita può essere piena di sfide, ma è anche piena di bellezza e gentilezza. Lasciando andare la sua rabbia e abbracciando la gratitudine, aveva trovato una felicità che non aveva mai conosciuto prima.

E così, Letizia visse il resto dei suoi giorni come un simbolo di amore e gioia, ricordando a tutti coloro che incontrava che la felicità è qualcosa che si crea da dentro. decise di portare Letizia in un'avventura nella foresta vicina. Sperava che un cambiamento di scenario potesse rallegrarla. Mentre camminavano attraverso la foresta, Letizia continuava a brontolare, senza notare gli uccellini che cantavano o i fiori vibranti che ondeggiavano nella brezza. All'improvviso, uno scoiattolo attraversò il loro cammino, facendo abbiare furiosamente Letizia che iniziò a inseguirlo. Corse e corse, addentrandosi sempre più nella foresta, fino a rendersi conto di essersi persa.
Spaventata, Letizia abbaiò e ululò, ma non ci fu nessuna risposta. Vagò per la foresta, la sua rabbia si trasformò in paura mentre il sole iniziava a tramontare. Proprio quando stava per perdere la speranza, inciampò in una piccola capanna diroccata. Disperata in cerca di aiuto, si avvicinò cautamente.

All'interno della capanna viveva un vecchio eremita di nome Gregorio. Era un uomo saggio che aveva scelto una vita di solitudine per connettersi con la natura e trovare la pace interiore. Quando vide Letizia, la accolse calorosamente, offrendole cibo e riparo. Letizia, sebbene ancora diffidente, accettò la sua gentilezza.

Nei giorni successivi, Gregorio e Letizia divennero amici improbabili. Gregorio aveva un dono con gli animali e con pazienza insegnò a Letizia la bellezza della foresta e l'importanza della pace interiore. Le raccontò storie delle sue stesse difficoltà e di come aveva imparato a trovare gioia nelle piccole cose.'''

text3 = '''

Una storia in particolare colpì profondamente Letizia. Gregorio raccontò di un tempo in cui era stato un giovane uomo, pieno di rabbia e risentimento. Aveva incolpato il mondo per le sue disgrazie fino a quando un giorno incontrò un vecchio viaggiatore che gli impartì una lezione profonda. Il viaggiatore disse: "La felicità non è qualcosa che trovi; è qualcosa che crei. Inizia da dentro."

Ispirata dalla storia di Gregorio, Letizia iniziò a vedere il mondo sotto una luce diversa. Cominciò ad apprezzare la bellezza della foresta e la gentilezza del suo nuovo amico. Piano piano, la sua rabbia iniziò a svanire, sostituita da un senso di gratitudine.

Una mattina, Letizia si svegliò trovando Gregorio intento a preparare una piccola borsa. "È ora che tu torni a casa, Letizia," disse dolcemente. "Hai imparato molto, e la signora Serena deve essere preoccupata per te."

Letizia sentì una fitta di tristezza all'idea di lasciare Gregorio, ma sapeva che aveva ragione. Con il cuore pesante, lo salutò e iniziò il suo viaggio di ritorno a casa. Mentre attraversava la foresta, non poteva fare a meno di notare quanto tutto sembrasse diverso. Gli alberi sembravano più verdi, i fiori avevano un profumo più dolce e persino i canti degli uccelli sembravano più melodiosi.

Quando Letizia finalmente uscì dalla foresta, vide la signora Serena che la aspettava ansiosamente. Vedendo Letizia, il volto della signora Serena si illuminò di gioia. "Oh, Letizia! Ero così preoccupata per te!" esclamò, abbracciandola strettamente.

Con sorpresa della signora Serena, Letizia rispose scodinzolando e facendo una carezza gentile. Non era più il cucciolo arrabbiato e scontroso che era stato prima. Letizia aveva imparato a trovare la felicità e la gratitudine nel suo cuore.

Da quel giorno in poi, la vita di Letizia cambiò in meglio. Divenne conosciuta come il cane più dolce e amorevole del paese. Fece amicizia con gli altri animali, giocò felicemente con i bambini e aiutò persino la signora Serena nel suo giardino.

Il viaggio di Letizia le aveva insegnato una lezione inestimabile: la vita può essere piena di sfide, ma è anche piena di bellezza e gentilezza. Lasciando andare la sua rabbia e abbracciando la gratitudine, aveva trovato una felicità che non aveva mai conosciuto prima.

E così, Letizia visse il resto dei suoi giorni come un simbolo di amore e gioia, ricordando a tutti coloro che incontrava che la felicità è qualcosa che si crea da dentro.'''

client = OpenAI()

with client.audio.speech.with_streaming_response.create(
    model="tts-1",
    voice="onyx",
    input=text1,
) as response:
    response.stream_to_file("speech1.mp3")

playsound('speech.mp3')
