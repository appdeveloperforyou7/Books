#!/usr/bin/env python3
# Generates content_v4.html — Chapter 9, Option C (all 34 verses; 6 deep-dived).
import io
BUILD = r'D:\Kapil\Books\Gita for non Hindus\build'

# ---- chapter accent colour (change per chapter) ----
ACCENTS = {
 'saffron': dict(accent='#C77A1A', tint='#FBF1E0', tint2='#F0DEB8'),
 'sage':    dict(accent='#3E9C73', tint='#EAF5EF', tint2='#CFE6DA'),
 'slate':   dict(accent='#335A8C', tint='#E9EFF7', tint2='#D2DDEC'),
 'plum':    dict(accent='#8C3A55', tint='#F3E7EB', tint2='#E2CFD7'),
 'gold':    dict(accent='#A9791A', tint='#FBF1DD', tint2='#EFE0B6'),
}
ACCENT = 'saffron'   # <-- set per chapter
A = ACCENTS[ACCENT]

# --- All 34 verses: (no, dev, iast, gist) ---
V = [
("9.1","इदं तु ते गुह्यतमं प्रवक्ष्याम्यनसूयवे ।<br>ज्ञानं विज्ञानसहितं यज्ञात्वा मोक्ष्यसेऽशुभात् ॥",
 "idaṃ tu te guhyatamaṃ pravakṣyāmy anasūyave / jñānaṃ vijñāna-sahitaṃ yaj jñātvā mokṣyase 'śubhāt",
 "Because you do not find fault, I will speak this most secret knowledge — knowing which you are freed from evil."),
("9.2","राजविद्या राजगुह्यं पवित्रमिदमुत्तमम् ।<br>प्रत्यक्षावगमं धर्म्यं सुसुखं कर्तुमव्ययम् ॥",
 "rāja-vidyā rāja-guhyam pavitram idam uttamam / pratyakṣāvagamaṃ dharmyaṃ su-sukhaṃ kartum avyayam",
 "The king of sciences, the king of secrets — purest, supreme, directly realised, righteous, joyful to practise, imperishable."),
("9.3","अश्रद्दधानाः पुरुषा धर्मस्यास्य परन्तप ।<br>अप्राप्य मां निवर्तन्ते मृत्युसंसारवर्त्मनि ॥",
 "aśraddadhānāḥ puruṣā dharmasyāsya parantapa / aprāpya māṃ nivartante mṛtyu-saṃsāra-vartmani",
 "Those without faith in this dharma, failing to reach Me, return to the path of death and rebirth."),
("9.4","मया ततमिदं सर्वं जगदव्यक्तमूर्तिना ।<br>मत्स्थानि सर्वभूतानि न चाहं तेष्ववस्थितः ॥",
 "mayā tatam idaṃ sarvaṃ jagad avyakta-mūrtinā / mat-sthāni sarva-bhūtāni na cāhaṃ teṣv avasthitaḥ",
 "By My unmanifest form all this universe is pervaded; all beings dwell in Me — yet I dwell not in them."),
("9.5","न च मत्स्थानि भूतानि पश्य मे योगमैश्वरम् ।<br>भूतभृन्न च भूतस्थो ममात्मा भूतभावनः ॥",
 "na ca mat-sthāni bhūtāni paśya me yogam aiśvaram / bhūta-bhṛn na ca bhūta-stho mamātmā bhūta-bhāvanaḥ",
 "Yet beings are not really in Me — behold My divine yoga: I sustain all without dwelling in them; My Self originates all beings."),
("9.6","यथाकाशस्थितो नित्यं वायुः सर्वत्रगो महान् ।<br>तथा सर्वाणि भूतानि मत्स्थानीत्युपधारय ॥",
 "yathā ākāśa-sthito nityaṃ vāyuḥ sarvatrago mahān / tathā sarvāṇi bhūtāni mat-sthānīty upadhāraya",
 "As the great wind, ever moving, rests in space — understand that all beings rest in Me."),
("9.7","सर्वभूतानि कौन्तेय प्रकृतिं यान्ति मामिकाम् ।<br>कल्पक्षये पुनस्तानि कल्पादौ विसृजाम्यहम् ॥",
 "sarva-bhūtāni kaunteya prakṛtiṃ yānti māmikām / kalpa-kṣaye punas tāni kalpādau visṛjāmy aham",
 "At a cosmic age's end all beings merge into My nature; at the new age's dawn I emit them again."),
("9.8","प्रकृतिं स्वामवष्टभ्य विसृजामि पुनः पुनः ।<br>भूतग्राममिमं कृत्स्नमवशं प्रकृतेर्वशात् ॥",
 "prakṛtiṃ svām avaṣṭabhya visṛjāmi punaḥ punaḥ / bhūta-grāmam imaṃ kṛtsnam avaśaṃ prakṛter vaśāt",
 "Taking hold of My own nature, again and again I project this whole multitude of beings, helpless under nature's sway."),
("9.9","न च मां तानि कर्माणि निबध्नन्ति धनञ्जय ।<br>उदासीनवदासीनमसक्तं तेषु कर्मसु ॥",
 "na ca māṃ tāni karmāṇi nibadhnanti dhanañjaya / udāsīna-vad āsīnam asaktaṃ teṣu karmasu",
 "These actions bind Me not, O Arjuna — I sit as one indifferent, unattached to those acts."),
("9.10","मयाध्यक्षेण प्रकृतिः सूयते सचराचरम् ।<br>हेतुनानेन कौन्तेय जगद्विपरिवर्तते ॥",
 "mayādhyakṣeṇa prakṛtiḥ sūyate sacarācaram / hetunānena kaunteya jagad viparyavartate",
 "Under My oversight nature brings forth all moving and unmoving things, and by this cause the world revolves."),
("9.11","अवजानन्ति मां मूढा मानुषीं तनुमाश्रितम् ।<br>परं भावमजानन्तो मम भूतमहेश्वरम् ॥",
 "avajānanti māṃ mūḍhā mānuṣīṃ tanum āśritam / paraṃ bhāvam ajānanto mama bhūta-maheśvaram",
 "Fools despise Me in My human body, not knowing My supreme nature as the great Lord of all beings."),
("9.12","मोघाशा मोघकर्माणो मोघज्ञाना विचेतसः ।<br>राक्षसीमासुरीं चैव प्रकृतिं मोहिनीं श्रिताः ॥",
 "moghāśā mogha-karmāṇo mogha-jñānā vicetasaḥ / rākṣasīm āsurīṃ caiva prakṛtiṃ mohinīṃ śritāḥ",
 "Their hopes, acts and knowledge are vain; bewildered, they cling to the delusive demoniac nature."),
("9.13","महात्मानस्तु मां पार्थ दैवीं प्रकृतिमाश्रिताः ।<br>भजन्त्यनन्यमनसो ज्ञात्वा भूतादिमव्ययम् ॥",
 "mahātmānas tu māṃ pārtha daivīṃ prakṛtim āśritāḥ / bhajanty ananya-manaso jñātvā bhūta-ādim avyayam",
 "But the great souls, grounded in the divine nature, worship Me with undivided mind, knowing Me as the imperishable source."),
("9.14","सततं कीर्तयन्तो मां यतन्तश्च दृढव्रताः ।<br>नमस्यन्तश्च मां भक्त्या नित्ययुक्ता उपासते ॥",
 "satataṃ kīrtayanto māṃ yatantaś ca dṛḍha-vratāḥ / namasyantaś ca māṃ bhaktyā nitya-yuktā upāsate",
 "Ever chanting My glories, striving with firm vows, bowing in devotion, they worship Me, ever united."),
("9.15","ज्ञानयज्ञेन चाप्यन्ये यजन्तो मामुपासते ।<br>एकत्वेन पृथक्त्वेन बहुधा विश्वतोमुखम् ॥",
 "jñāna-yajñena cāpy anye yajanto mām upāsate / ekatvena pṛthaktvena bahudhā viśvato-mukham",
 "Others worship Me by the sacrifice of knowledge — as the One, as the many, in diverse ways, the all-faced universal Being."),
("9.16","अहं क्रतुरहं यज्ञः स्वधाहमहमौषधम् ।<br>मन्त्रोऽहमहमेवाज्यमहमग्निरहं हुतम् ॥",
 "ahaṃ kratur ahaṃ yajñaḥ svadhāham aham auṣadham / mantro'ham aham evājyam aham agnir ahaṃ hutam",
 "I am the rite, the sacrifice, the offering to the ancestors, the healing herb, the mantra, the clarified butter, the fire and the oblation."),
("9.17","पिताहमस्य जगतो माता धाता पितामहः ।<br>वेद्यं पवित्रमोंकार ऋक् साम यजुरेव च ॥",
 "pitāham asya jagato mātā dhātā pitāmahaḥ / vedyaṃ pavitram oṁkāra ṛk sāma yajur eva ca",
 "Father, mother, sustainer, grandsire of this world; the knowable, the purifier, the syllable Oṁ, the Ṛg, Sāma and Yajur Veda."),
("9.18","गतिर्भर्ता प्रभुः साक्षी निवासः शरणं सुहृत् ।<br>प्रभवः प्रलयः स्थानं निधानं बीजमव्ययम् ॥",
 "gatir bhartā prabhuḥ sākṣī nivāsaḥ śaraṇaṃ suhṛt / prabhavaḥ pralayaḥ sthānaṃ nidhānaṃ bījam avyayam",
 "Goal, supporter, Lord, witness, abode, refuge, friend; origin, dissolution, ground, resting-place and the imperishable seed."),
("9.19","तपाम्यहमहं वर्षं निगृह्णाम्युत्सृजामि च ।<br>अमृतं चैव मृत्युश्च सदसच्चाहमर्जुन ॥",
 "tapāmy aham ahaṃ varṣaṃ nigṛhṇāmy utsṛjāmi ca / amṛtaṃ caiva mṛtyuś ca sad asac cāham arjuna",
 "I send forth heat; I withhold and release the rain; I am immortality and death, O Arjuna — both being and non-being."),
("9.20","त्रैविद्या मां सोमपाः पूतपापा<br>यज्ञैरिष्ट्वा स्वर्गतिं प्रार्थयन्ते ।<br>ते पुण्यमासाद्य सुरेन्द्रलोकमश्नन्ति दिव्यान्दिवि देवभोगान् ॥",
 "traividya māṃ somapāḥ pūta-pāpā yajñair iṣṭvā svarga-gatiṃ prārthayante / te puṇyam āsādya surendra-lokam aśnanti divyān divi deva-bhogān",
 "Knowers of the three Vedas, cleansed of sin, worship Me by sacrifice and seek heaven; attaining merit, they enjoy the delights of Indra's world."),
("9.21","ते तं भुक्त्वा स्वर्गलोकं विशालं<br>क्षीणे पुण्ये मर्त्यलोकं विशन्ति ।<br>एवं त्रयीधर्ममनुप्रपन्ना गतागतं कामकामा लभन्ते ॥",
 "te taṃ bhuktvā svarga-lokaṃ viśālaṃ kṣīṇe puṇye martya-lokaṃ viśanti / evaṃ trayī-dharma anuprapannā gatāgataṃ kāma-kāmā labhante",
 "Having enjoyed that vast heaven, when merit is exhausted they fall back to the mortal world — so desire-driven Vedic worshippers gain only round-trip coming and going."),
("9.22","अनन्याश्चिन्तयन्तो मां ये जनाः पर्युपासते ।<br>तेषां नित्याभियुक्तानां योगक्षेमं वहाम्यहम् ॥",
 "ananyāś cintayanto māṃ ye janāḥ paryupāsate / teṣāṃ nityābhiyuktānāṃ yoga-kṣemaṃ vahāmy aham",
 "Those who, thinking of nothing else, ever worship Me — to those ever-united ones I Myself bear their yoga and kṣema."),
("9.23","येऽप्यन्यदेवता भक्ता यजन्ते श्रद्धयान्विताः ।<br>तेऽपि मामेव कौन्तेय यजन्त्यविधिपूर्वकम् ॥",
 "ye'py anya-devatā-bhaktā yajante śraddhayānvitāḥ / te'pi mām eva kaunteya yajanty avidhi-pūrvakam",
 "Even devotees of other gods worship with faith — they too worship Me, Kaunteya, though by an indirect path."),
("9.24","अहं हि सर्वयज्ञानां भोक्ता च प्रभुरेव च ।<br>न तु मामभिजानन्ति तत्त्वेनातश्च्यवन्ति ते ॥",
 "ahaṃ hi sarva-yajñānāṃ bhoktā ca prabhur eva ca / na tu mām abhijānanti tattvenātas cyavanti te",
 "I alone am the enjoyer and Lord of every sacrifice; not knowing Me in truth, they fall."),
("9.25","यान्ति देवव्रता देवान् पितॄन्यान्ति पितृव्रताः ।<br>भूतानि यान्ति भूतेज्या यान्ति मद्याजिनोऽपि माम् ॥",
 "yānti deva-vratā devān pitṝn yānti pitṛ-vratāḥ / bhūtāni yānti bhūtejyā yānti mad-yājino'pi mām",
 "Worshippers of the gods go to the gods; of the ancestors, to the ancestors; of the spirits, to the spirits — but My worshippers come to Me."),
("9.26","पत्रं पुष्पं फलं तोयं यो मे भक्त्या प्रयच्छति ।<br>तदहं भक्त्युपहृतमश्नामि प्रयतात्मनः ॥",
 "patraṃ puṣpaṃ phalaṃ toyaṃ yo me bhaktyā prayacchati / tad ahaṃ bhakty-upahṛtam aśnāmi prayatātmanaḥ",
 "Whoever offers Me a leaf, a flower, a fruit, or water with devotion — that devoted offering I accept from a pure-hearted one."),
("9.27","यत्करोषि यदश्नासि यज्जुहोषि ददासि यत् ।<br>यत्तपस्यसि कौन्तेय तत्कुरुष्व मदर्पणम् ॥",
 "yat karoṣi yad aśnāsi yaj juhoṣi dadāsi yat / yat tapasyasi kaunteya tat kuruṣva mad-arpaṇam",
 "Whatever you do, eat, offer, or give, and whatever austerity you practise — do it as an offering to Me."),
("9.28","शुभाशुभफलैरेवं मोक्ष्यसे कर्मबन्धनैः ।<br>संन्यासयोगयुक्तात्मा विमुक्तो मामुपैष्यसि ॥",
 "śubhāśubha-phalair evaṃ mokṣyase karma-bandhanaiḥ / saṃnyāsa-yoga-yuktātmā vimukto mām upaiṣyasi",
 "Thus you shall be freed from the bondage of good and bad fruits; united by the yoga of renunciation, liberated, you attain Me."),
("9.29","समोऽहं सर्वभूतेषु न मे द्वेष्योऽस्ति न प्रियः ।<br>ये भजन्ति तु मां भक्त्या मयि ते तेषु चाप्यहम् ॥",
 "samo'haṃ sarva-bhūteṣu na me dveṣyo'sti na priyaḥ / ye bhajanti tu māṃ bhaktyā mayi te teṣu cāpy aham",
 "I am the same to all beings; none is hateful, none dear — yet those who worship Me in devotion are in Me, and I in them."),
("9.30","अपि चेत्सुदुराचारो भजते मामनन्यभाक् ।<br>साधुरेव स मन्तव्यः सम्यग्व्यवसितो हि सः ॥",
 "api cet su-durācāro bhajate mām ananya-bhāk / sādhur eva sa mantavyaḥ samyag vyavasito hi saḥ",
 "Even one of very evil conduct, who worships Me with single-minded devotion, is to be regarded as righteous — for he is truly resolved."),
("9.31","क्षिप्रं भवति धर्मात्मा शश्वच्छान्तिं निगच्छति ।<br>कौन्तेय प्रति जानीहि न मे भक्तः प्रणश्यति ॥",
 "kṣipraṃ bhavati dharmātmā śaśvac-chāntiṃ nigacchati / kaunteya prati jānīhi na me bhaktaḥ praṇaśyati",
 "He quickly becomes righteous and attains eternal peace — know for certain, Kaunteya: My devotee never perishes."),
("9.32","मां हि पार्थ व्यपाश्रित्य येऽपि स्युः पापयोनयः ।<br>स्त्रियो वैश्यास्तथा शूद्रास्तेऽपि यान्ति परां गतिम् ॥",
 "māṃ hi pārtha vyapāśritya ye'pi syuḥ pāpa-yonayaḥ / striyo vaiśyās tathā śūdrās te'pi yānti parāṃ gatim",
 "Taking refuge in Me, even those of disadvantaged birth — women, vaiśyas, śūdras too — attain the supreme goal."),
("9.33","किं पुनर्ब्राह्मणाः पुण्या भक्ता राजर्षयस्तथा ।<br>अनित्यमसुखं लोकमिमं प्राप्य भजस्व माम् ॥",
 "kiṃ punar brāhmaṇāḥ puṇyā bhaktā rājarṣayas tathā / anityam asukhaṃ lokam imaṃ prāpya bhajasva mām",
 "How much more, then, the pure brāhmaṇas and royal sages who are devoted! Having come to this transient, joyless world — worship Me."),
("9.34","मन्मना भव मद्भक्तो मद्याजी मां नमस्कुरु ।<br>मामेवैष्यसि युक्त्वैवमात्मानं मत्परायणः ॥",
 "man-manā bhava mad-bhakto mad-yājī māṃ namaskuru / mām evaiṣyasi yuktvāivam ātmānaṃ mat-parāyaṇaḥ",
 "Fix your mind on Me, be My devotee, sacrifice to Me, bow to Me; thus offering your self to Me, you shall come to Me."),
]
V = {n:(d,i,g) for (n,d,i,g) in V}

# plain 1-2 line meaning (non-Hindu-friendly gloss) for each compact verse
M = {
"9.1":"The Gītā's most important teaching is being offered now — and the only requirement is an open, non-judgemental mind.",
"9.2":"This knowledge is the highest of all: it purifies, is directly experienced, easy to live, and once grasped, never fades.",
"9.3":"Without trust in the teaching, no progress is possible; the sceptic stays bound to the round of birth and death.",
"9.4":"God holds all things within himself, yet is not contained by them — present everywhere, trapped nowhere.",
"9.5":"A paradox of intimacy: he sustains every being without being lodged inside any of them.",
"9.6":"Like wind moving within space — everything moves within him, dependent on him, while he remains free.",
"9.7":"At each cosmic cycle's end all beings dissolve into nature; at the next dawn he sends them forth again.",
"9.8":"He is the quiet power behind creation's rhythm, projecting all beings — yet he himself remains unaffected.",
"9.9":"Though all action flows from him, he is never bound by it: indifferent, unattached, free.",
"9.11":"Those who see only a human body miss the divinity standing right before them.",
"9.12":"Deluded minds chase empty hopes and end in darkness, deceived by their own restless nature.",
"9.13":"The truly great turn wholly toward the Divine, knowing him as the deathless source of all that exists.",
"9.14":"Their lives become one continuous act of remembrance — chanting, striving, bowing, devoted.",
"9.15":"Seekers approach the One in many ways — as the single Reality, as the many, as the all-pervading whole.",
"9.16":"Every element of worship — the rite, the fire, the offering, the very words — is himself.",
"9.17":"He is the parent, support and meaning of the whole world, and the sound Oṁ that names it.",
"9.18":"Whatever you seek — a refuge, a friend, a foundation, the seed of all things — he is that.",
"9.19":"He is the weather of existence itself: the rain and heat, life and death, being and not-being.",
"9.20":"Ritual-seekers reach a temporary heaven as a reward and enjoy its pleasures while they last.",
"9.21":"But when the merit runs out they fall back to earth — desire-driven worship earns only round-trips, never freedom.",
"9.23":"Sincerity, not the correct name, is what reaches the Divine — even worship of 'other gods' comes to him.",
"9.24":"He alone receives every offering made anywhere; to miss this truth is to fall short.",
"9.25":"You reach what you worship — the gods, the ancestors, the spirits — but his devotee reaches him alone.",
"9.27":"Make your whole life an offering: every act, meal, gift, and discipline, given to him.",
"9.28":"Offered thus, action no longer binds; the detached doer is freed and reaches the Divine.",
"9.32":"No birth, gender, or status bars the way — whoever takes refuge attains the highest goal.",
"9.33":"If even the disadvantaged can reach him, how much more the devoted and the pure — therefore, worship.",
}

# group dividers inserted BEFORE a verse number:  (before_verse, label)
DIV = [
 ("9.1","9.1 – 9.9 · The most secret knowledge, and how the world is run"),
 ("9.11","9.11 – 9.21 · The great souls — and those who seek lesser heavens"),
 ("9.23","9.23 – 9.25 · Every sincere prayer reaches the One"),
 ("9.27","9.27 – 9.28 · Offer every act, and be free"),
 ("9.32","9.32 – 9.33 · No one is excluded from the supreme"),
]

def tag(letter, cls):
    return f'<span class="tl {cls}">{letter}</span>'

def box(cls, head, body):
    return f'<div class="box {cls}"><div class="h">{head}</div><p>{body}</p></div>'

def legend():
    def chip(letter, color):
        return f'<span class="tl" style="background:{color};">{letter}</span>'
    rows = ""
    for (l,cls,rest) in [("P","p","how to say the Sanskrit (transliteration)."),
                         ("L","l","a close, word-faithful translation."),
                         ("M","m","what it says, in plain English."),
                         ("C","c","the philosophical point (opened verses).")]:
        rows += f'<p>{tag(l,cls)}&nbsp; <b>{l}</b> — {rest}</p>'
    return ('<div class="legend"><div class="lh">How to read the verses</div>'
            '<p>Every verse appears in <b>Sanskrit</b>, then three short lines marked '
            f'{tag("P","p")} {tag("L","l")} {tag("M","m")} — pronunciation, literal, meaning. '
            'A few key verses are <b>opened</b> in a shaded block with extra layers:</p>'
            f'<p>{chip("▸","#A9791A")} For the non-Hindu reader &nbsp; '
            f'{chip("▸","#8C3A55")} Try this (practice) &nbsp; '
            f'{chip("▸","#335A8C")} Going deeper &nbsp; '
            f'{chip("▸","#A84E29")} A common misreading.</p>'
            + rows + '</div>')

# deep-dive content keyed by verse-no (or range)
DEEP = {
"9.10": dict(title="How the world runs — God as the silent overseer",
  literal="Under Me as overseer, Nature (prakṛti) brings forth the moving and the unmoving; by this cause, O Arjuna, the universe revolves.",
  plain="The whole world is not running itself, and it is not running you. There is an intelligence behind it — not pushing from outside like a mechanic, but pervading from within like the stillness at the centre of a wheel. Everything that grows, moves, and changes is nature doing its work; but nature itself is watched over by something that does not change.",
  commentary="This single verse quietly dissolves two errors at once. It rejects the idea of a remote, absentee God (he is <em>adhyakṣa</em>, “the overseer,” right here) and the idea that the material world is itself divine (<em>prakṛti</em> does the producing; he supervises it).",
  bridge="Think of a great conductor. The musicians make every sound; the conductor makes none. Yet without the conductor’s silent presence, the music falls apart. Krishna is not a note in the symphony — he is what holds the symphony together.",
  sadhana_h="watch for the “overseer”", sadhana="Today, pick one ordinary process — a plant growing, your breath, the turning of the day — and instead of seeing only the surface, sense the still intelligence within it. The practice of Chapter 9 begins here: in <em>recognizing</em> that you are watched over, not in <em>earning</em> it.",
  adept="<em>prakṛti</em> (प्रकृति) = primordial nature; <em>adhyakṣa</em> (अध्यक्ष) = “over-seer,” from <em>adhi</em> + <em>akṣa</em> (eye). The Sāṃkhya schools read this as pure dualism (matter vs. spirit); the bhakti schools read Krishna himself as the <em>adhyakṣa</em> — the hinge where impersonal philosophy turns personal."),
"9.22": dict(title="THE PROMISE",
  literal="Those who, thinking of nothing else, ever-worship Me with undivided devotion — to those ever-united ones I Myself carry their yoga-kṣema.",
  plain="If you keep your mind on Me — not as one thing among many, but as the centre — then your needs become My responsibility. I carry what you have not yet acquired (<em>yoga</em>) and I protect what you already hold (<em>kṣema</em>).",
  commentary="Notice what it does <em>not</em> say. It does not promise wealth, success, or comfort. It promises that <em>the One behind the universe personally undertakes your welfare.</em> The condition is precise: <em>ananyāḥ</em> — “without another.” Not that you must think of God every second, but that he is your <em>refuge</em>, the fixed star by which you navigate. To such a one, the cosmic Lord becomes a porter.",
  bridge="Every parent knows this promise from the other side. A small child does not earn its food or fear the rent; it simply trusts the one who carries it. Chapter 9 says the universe is built on that same trust — and God is the one carrying.",
  sadhana_h="the handover practice", sadhana="Once a day — at a moment of genuine anxiety — deliberately hand one worry over. Say inwardly: “This is now Yours.” The verse is not a theory to believe; it is an experiment to run. Run it for thirty days and watch what changes — not in the world, but in you.",
  warn_h="What it is NOT", warn="This is <b>not</b> a prosperity teaching. Krishna is not a cosmic ATM. <em>Yoga-kṣema</em> means your <em>true</em> welfare — which may include hardship that saves you, and loss that frees you. To read it as “devotion gets you riches” is to make the Gītā small."),
"9.26": dict(title="The smallest offering",
  literal="Whoever offers Me a leaf, a flower, a fruit, or water with devotion — that devoted offering, from a pure-hearted one, I accept.",
  plain="You do not need a temple, a priest, or a fortune. A single leaf, offered with love, is enough. God is not impressed by the size of the gift but by the size of the heart behind it.",
  commentary="This verse democratized Indian spirituality forever. After 9.26, no one is too poor to worship. The emphasis falls entirely on <em>bhakti</em> (devotion) and <em>prayatātman</em> (a pure, concentrated heart). The leaf and the water are metaphors for <em>anything offered wholeheartedly</em> — your work, your attention, your forgiveness of someone who hurt you.",
  bridge="A child’s crayon drawing, given with love, is treasured by a parent more than a gallery masterpiece bought by a stranger. The economy of love runs on a different currency than the economy of things.",
  sadhana_h="the leaf practice", sadhana="Offer one small thing today <em>as if to God</em> — a cup of tea, a few quiet breaths, an act of kindness done in secret. Not for reward; simply given. Do this and you are already performing the central ritual of Chapter 9."),
"9.29": dict(title="The equality of God",
  plain="God plays no favourites. He does not love the saint more than the sinner, the priest more than the outcast. But those who <em>turn</em> toward him in love enter a different relationship: they abide in him, and he in them.",
  warn_h="What it is NOT", warn="“None hateful, none dear” is <b>not</b> indifference. It means God’s care is not rationed by rank, birth, or virtue — which is precisely what makes the devotion of the next two verses so radical."),
"9.30-31": dict(title="Grace for the fallen — the chapter’s climax",
  plain="You are not your worst day. No matter how far you have fallen, the moment you turn your whole heart toward the Divine — that very moment — you are already counted among the good. And from that turning, you will <em>become</em> good, soon, and find a peace that does not pass away. This is a guarantee.",
  commentary="These two verses are the moral centre of the entire Gītā. They overturn a religion of earned salvation and announce a religion of grace. The Sanskrit is striking: <em>sādhur eva sa mantavyaḥ</em> — “he is <em>to be regarded</em> as righteous.” Krishna commands <em>us</em> to change how we see the struggling sinner who has turned. And <em>kṣipraṃ bhavati dharmātmā</em> — “he quickly becomes righteous”: the turning is not the end but the beginning of transformation. Grace is the starting line, not the finish.",
  bridge="Every recovery tradition on earth has discovered this. “One day at a time.” The admission of powerlessness is not the proof of failure — it is the door. The Gītā said it first: the sincere turn, however late, however messy, is met.",
  sadhana_h="the prodigal practice", sadhana="If there is a part of yourself you have written off as “too far gone,” take one minute today and offer even <em>that</em> — your failure, your shame — to the Divine, not to be fixed but to be held. The verse promises not that you are already clean, but that you are <em>counted</em> as on the way. Live as the one you are becoming, not the one you were.",
  adept_h="how the schools read this", adept="<b>Rāmānuja</b> — salvation by grace alone (<i>prapatti</i>): the path for those who cannot climb by knowledge.<br><b>Śaṅkara</b> — devotion <i>ignites</i> the knowledge that purifies; grace and effort are partners, not rivals.<br><b>In sum</b> — the Gītā holds both: grace receives you, practice transforms you."),
"9.34": dict(title="the chapter’s closing call",
  plain="Four verbs, one path: <em>think of Me, love Me, offer to Me, surrender to Me.</em> Do this, and the distance between you and the Divine — which only ever existed in your mind — dissolves.",
  sadhana_h="the four-breath practice", sadhana="Breathe in: <em>remember.</em>&nbsp; Breathe out: <em>love.</em>&nbsp; Breathe in: <em>offer.</em>&nbsp; Breathe out: <em>let go.</em> Four breaths, four verbs, the entire chapter in your body. Use it before sleep, before a hard conversation, before anything that asks for more than you think you have."),
}

def verse_panel(n):
    d,i,_g = V[n]
    return f'<div class="verse"><div class="dev">{d}</div><div class="iast">{i}</div><div class="vno">GĪTĀ {n}</div></div>'

def combined_panel(n):
    d1,i1,_ = V["9.30"]; d2,i2,_ = V["9.31"]
    return ('<div class="verse"><div class="dev">'+d1+d2+'</div>'
            '<div class="iast">'+i1+' / '+i2+'</div>'
            '<div class="vno">GĪTĀ '+n+'</div></div>')

def compact(n):
    d,i,g = V[n]
    m = M.get(n,"")
    return (f'<div class="cv"><div class="cvn">{n}</div><div class="cvt">'
            f'<div class="devc">{d}</div>'
            f'<div class="ln">{tag("P","p")}<span class="tx iastc">{i}</span></div>'
            f'<div class="ln">{tag("L","l")}<span class="tx litc">{g}</span></div>'
            f'<div class="ln">{tag("M","m")}<span class="tx meanc">{m}</span></div>'
            f'</div></div>')

def deep(n):
    dd = DEEP[n]
    out = ['<div class="vunit">']
    out.append(f'<div class="vh"><span class="badge">{n}</span><span class="vht">{dd["title"]}</span></div>')
    out.append('<div class="vcore">'+(combined_panel(n) if "-" in n else verse_panel(n))+'</div>')
    out.append('<div class="vbody">')
    if "literal" in dd:
        out.append('<div class="ln2">'+tag("L","l")+'<span class="labx">Literal</span></div><p>'+dd["literal"]+'</p>')
    if "plain" in dd:
        out.append('<div class="ln2">'+tag("M","m")+'<span class="labx">In plain English</span></div><p>'+dd["plain"]+'</p>')
    if "commentary" in dd:
        out.append('<div class="ln2">'+tag("C","c")+'<span class="labx">Commentary</span></div><p>'+dd["commentary"]+'</p>')
    if "bridge" in dd: out.append(box("bridge","For the new reader",dd["bridge"]))
    if "sadhana" in dd: out.append(box("sadhana","Try this — "+dd.get("sadhana_h","a practice"),dd["sadhana"]))
    if "adept" in dd: out.append(box("adept","Going deeper — "+dd.get("adept_h","roots & commentaries"),dd["adept"]))
    if "warn" in dd: out.append(box("warn","A common misreading",dd["warn"]))
    out.append('</div></div>')
    return "\n".join(out)

def section(num, title):
    return (f'<div class="sec"><span class="secn">{num}</span>'
            f'<span class="sect">{title}</span></div>')

def groupdiv(label):
    return f'<div class="grp">{label}</div>'

# ---- assemble body ----
body = []
body.append(section("1","Intro Card"))
body.append('<p class="lead"><b>What happens.</b> Krishna calls what he is about to say <em>rāja-vidyā rāja-guhya</em> — “the king of knowledge and the king of secrets.” He reveals how he pervades the universe without being contained by it; how every form of worship finally reaches him; and then he makes the most tender promise in the scripture: <em>to the one who remembers him with an undivided heart, he himself carries what they lack and guards what they have.</em> It ends with the most radical grace of all: even a person sunk in wrongdoing, if they turn to him with wholehearted love, are quickly made righteous.</p>')
body.append('<p class="lead"><b>Why this chapter matters to you.</b> If the Gītā so far has been a map, Chapter 9 is the moment the guide stops pointing at the mountain and takes your hand.</p>')

body.append(section("2","The Big Picture"))
body.append('<p class="noind">Three ideas hold Chapter 9 together, and each overturns a common assumption:</p>')
body.append('<ol class="bigpic">'
 '<li><b class="lead-saff">God is everywhere, but is not everything.</b> The world is <em>in</em> him; he is not reduced <em>to</em> the world. Neither strict monotheism nor pantheism — something more subtle, and more intimate.</li>'
 '<li><b class="lead-saff">Every sincere prayer reaches the same shore.</b> “Even those who worship other gods, with faith — they worship me alone, though they know it not.” The form matters less than the sincerity.</li>'
 '<li><b class="lead-saff">Grace is for the fallen, not only for the pure.</b> Even one of very evil conduct, if devoted, is counted righteous — and soon becomes so. The Gītā does not demand that you arrive clean. It asks only that you turn.</li></ol>')
body.append('<p>Read this chapter as an answer to a silent fear every honest person carries: <em>Am I too far gone?</em> Chapter 9’s answer is the heart of the whole book.</p>')

body.append(section("3","The Verses"))
body.append('<p class="noind" style="color:var(--muted);font-size:9.5pt;font-style:italic;margin-bottom:8pt">All 34 verses of the chapter are given below in Sanskrit and translation. Six key verses are opened in full — translation, commentary, a bridge for the new reader, and a practice.</p>')

deepset = {"9.10","9.22","9.26","9.29","9.30-31","9.34"}
# render order: 9.1..9.34, but 9.30 & 9.31 collapse into the 9.30-31 deep block
order = [f"9.{i}" for i in range(1,35)]
skip = set()
for n in order:
    if n in skip: continue
    for (bv,label) in DIV:
        if bv == n:
            body.append(groupdiv(label))
    if n == "9.30":
        body.append(deep("9.30-31")); skip.add("9.31"); continue
    if n in deepset:
        body.append(deep(n))
    else:
        body.append(compact(n))

body.append(section("4","Takeaway"))
body.append('<h2 class="sec2">Chapter 9 turns the Gītā from teaching into trust.</h2>')
body.append('<div class="takeaway"><ol>'
 '<li><b>You are overseen, not abandoned.</b> The universe has a centre, and it holds you.</li>'
 '<li><b>Your sincere prayer is enough — in any form.</b> God is not the property of one religion.</li>'
 '<li><b>You are never too far gone to turn.</b> Grace meets you the moment you turn, and carries you from there.</li></ol>'
 '<p class="close">The “king of secrets” is not a doctrine. It is the discovery that the power behind the cosmos is personal, patient, and closer than your own breath.</p></div>')

body.append(section("5","The 18-Step Sādhana Path — where you are"))
body.append('<p><b>Step 9 of 18 · OFFER A SINGLE LEAF.</b> This week, take the three Layer-2 practices of this chapter — <em>the overseer, the handover, the leaf</em> — and make them one daily act: offer one small thing each day, wholeheartedly, to the Divine. By week’s end, notice whether your sense of being <em>carried</em> (9.22) has quietly begun to come true. Then turn the page to Chapter 10, where Krishna shows you <em>where</em> to find him in the world around you.</p>')
body.append('<div class="path-note">Reader’s path: Wayfarer · Student · Seeker · Adept — this chapter contained all four. Re-read at a higher layer any time.</div>')

CSS = """
@page { size: 8in 10in; margin: 0.78in 0.8in 0.82in 0.82in; }
*{ box-sizing:border-box; }
:root{
  --accent:"""+A['accent']+r"""; --accent-tint:"""+A['tint']+r"""; --accent-tint2:"""+A['tint2']+r""";
  --ink:#1c1b2b; --paper:#FAF6EC;
  --plum:#8C3A55; --plum-tint:#F3E7EB;
  --slate:#335A8C; --slate-tint:#E9EFF7;
  --warn:#A84E29; --warn-tint:#FBEEE3;
  --rule:#DBCBA6; --muted:#5b5040;
}
html,body{ margin:0; padding:0; background:var(--paper); color:var(--ink); }
body{ font-family:'Noto Serif','Source Serif 4',Georgia,serif; font-size:10.5pt; line-height:1.48; }
p{ margin:0 0 8pt 0; text-align:justify; text-indent:13pt; hyphens:auto; }
p.lead,p.noind,.box p,.verse+p,li p,.cv p{ text-indent:0; }
p.lead{ font-size:11.5pt; line-height:1.5; margin-bottom:10pt; }
em{ color:#4a3f6b; } b,strong{ font-weight:700; }

/* === LEVEL 1: macro section === */
.sec{ display:flex; align-items:center; gap:10pt; border-bottom:1.4pt solid var(--accent);
  padding-bottom:6pt; margin:20pt 0 11pt 0; break-after:avoid; }
.sec .secn{ font-family:'Inter',sans-serif; font-size:11pt; font-weight:700; color:#fff;
  background:var(--accent); border-radius:50%; width:18pt; height:18pt; display:inline-flex;
  align-items:center; justify-content:center; flex:0 0 18pt; line-height:1; }
.sec .sect{ font-family:'Source Serif 4',serif; font-size:15.5pt; font-weight:700; color:var(--ink); letter-spacing:.01em; }
h2.sec2{ font-family:'Source Serif 4',serif; font-size:16pt; font-weight:700; margin:2pt 0 9pt 0; }
/* === LEVEL 2: group divider === */
.grp{ font-family:'Inter',sans-serif; font-size:7.5pt; font-weight:600; letter-spacing:.16em;
  text-transform:uppercase; color:#9a8a5e; text-align:center; margin:16pt 0 8pt 0;
  display:flex; align-items:center; gap:8pt; break-after:avoid; }
.grp::before,.grp::after{ content:""; flex:1; border-top:.6pt solid var(--rule); }

/* === layers legend === */
.legend{ background:#F4ECDB; border:0.7pt solid #E0CFA4; border-radius:4pt; padding:10pt 13pt; margin:6pt 0 12pt 0; break-inside:avoid; }
.legend .lh{ font-family:'Inter',sans-serif; font-size:7.5pt; font-weight:700; letter-spacing:.16em; text-transform:uppercase; color:#8a7a4e; margin-bottom:5pt; }
.legend p{ font-size:9pt; line-height:1.4; text-align:left; text-indent:0; margin-bottom:4pt; }
.legend .lt{ display:inline-flex; align-items:center; gap:4pt; font-weight:600; }

/* === LEVEL 3: deep-dive unit (grouped block) === */
.vunit{ background:#F7F0E0; border:0.7pt solid #E4D4AC; border-radius:5pt; padding:9pt 14pt 7pt; margin:8pt 0 10pt 0; }
.vh{ display:flex; align-items:center; gap:8pt; margin:0 0 6pt 0; break-after:avoid; }
.vh .badge{ font-family:'Inter',sans-serif; font-size:9pt; font-weight:700; color:#fff;
  background:var(--accent); padding:2pt 9pt; border-radius:9pt; letter-spacing:.04em; }
.vh .vht{ font-family:'Inter',sans-serif; font-size:8pt; font-weight:700; letter-spacing:.14em;
  text-transform:uppercase; color:var(--accent); }
.vcore{ break-inside:avoid; }
.vbody{ margin:3pt 0 4pt 18pt; padding-left:0; }
.vbody p{ font-size:9.6pt; text-align:left; }
.ln2{ display:flex; align-items:center; gap:5pt; margin:8pt 0 1pt 0; break-after:avoid; }
.labx{ font-family:'Inter',sans-serif; font-size:7pt; font-weight:700; letter-spacing:.16em;
  text-transform:uppercase; color:var(--muted); }
.verse{ background:var(--accent-tint); border-radius:3pt;
  padding:11pt 16pt 9pt 16pt; margin:4pt 0 9pt 0; break-inside:avoid; }
.verse .dev{ font-family:'Noto Serif Devanagari','Noto Sans Devanagari',serif; font-size:14.5pt; line-height:1.75;
  text-align:center; font-weight:600; color:#241f2e; margin:0 0 4pt 0; }
.verse .iast{ font-family:'Noto Serif','Source Serif 4',serif; font-style:italic; font-size:9.5pt;
  text-align:center; color:#6a5526; margin:0 0 5pt 0; line-height:1.4; }
.verse .vno{ font-family:'Inter',sans-serif; font-size:7pt; font-weight:700; letter-spacing:.14em; text-align:center; color:var(--accent); }
/* tiny circular line-tags: P pronunciation, L literal, M meaning, C commentary */
.tl{ display:inline-flex; align-items:center; justify-content:center; width:11pt; height:11pt; border-radius:50%;
  font-family:'Inter',sans-serif; font-size:6.5pt; font-weight:700; color:#fff; flex:0 0 11pt; line-height:1; }
.tl.p{ background:#9a8a5e; } .tl.l{ background:var(--slate); } .tl.m{ background:var(--accent); } .tl.c{ background:var(--plum); }
/* === LEVEL 4: compact verse === */
.cv{ display:flex; gap:9pt; margin:5pt 0; padding:6pt 0 6pt 0; border-bottom:.4pt dotted var(--rule); break-inside:avoid; }
.cv .cvn{ font-family:'Inter',sans-serif; font-size:8pt; font-weight:700; color:var(--accent); flex:0 0 26pt; padding-top:1pt; letter-spacing:.04em;}
.cv .cvt{ flex:1; }
.cv .devc{ font-family:'Noto Serif Devanagari','Noto Sans Devanagari',serif; font-size:11pt; line-height:1.55; color:#2a2433; margin-bottom:3pt; }
.cv .ln{ display:flex; align-items:baseline; gap:5pt; margin:1.5pt 0; }
.cv .tx{ flex:1; }
.cv .iastc{ font-family:'Noto Serif','Source Serif 4',serif; font-style:italic; font-size:8pt; color:#6a5526; }
.cv .litc{ font-size:8.6pt; color:#3a3340; line-height:1.32; }
.cv .meanc{ font-size:8.6pt; color:#5a4a2a; line-height:1.32; font-style:italic; }
/* === callout boxes (no bars; fill only) === */
.box{ border-radius:3pt; padding:9pt 12pt; margin:8pt 0; break-inside:avoid; }
.box p{ font-size:9.6pt; line-height:1.4; text-align:left; }
.box .h{ font-family:'Inter',sans-serif; font-size:7pt; font-weight:700; letter-spacing:.16em; text-transform:uppercase; margin-bottom:3pt; }
.box .h::before{ content:""; display:inline-block; width:5pt; height:5pt; margin-right:6pt; vertical-align:1pt; }
.bridge{ background:#FFF6E4; } .bridge .h{ color:#A9791A; } .bridge .h::before{ background:#A9791A; }
.sadhana{ background:var(--plum-tint); } .sadhana .h{ color:var(--plum); } .sadhana .h::before{ background:var(--plum); }
.adept{ background:var(--slate-tint); } .adept .h{ color:var(--slate); } .adept .h::before{ background:var(--slate); }
.warn{ background:var(--warn-tint); } .warn .h{ color:var(--warn); } .warn .h::before{ background:var(--warn); }
.bigpic li{ margin-bottom:9pt; line-height:1.44; } .bigpic li b.lead-saff{ color:var(--accent); }
.takeaway{ background:var(--accent-tint); border:1.4pt solid var(--accent); border-radius:4pt; padding:13pt 17pt; margin-top:5pt; break-inside:avoid; }
.takeaway ol{ margin:6pt 0 0 0; padding-left:17pt; } .takeaway li{ margin-bottom:6pt; } .takeaway .close{ font-style:italic; margin-top:6pt; }
.path-note{ font-family:'Inter',sans-serif; font-size:8pt; color:#7a6b48; font-style:italic; margin-top:12pt; border-top:.6pt solid var(--rule); padding-top:6pt; }
"""

def wrap(chunk):
    return ("<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'>"
            "<title>ch9 part</title><style>"+CSS+"</style></head><body>"
            + "\n".join(chunk) + "</body></html>")

# split into chunks to dodge Chrome's large-document font-subset bug
NPARTS = 5
cuts = [int(round(i*len(body)/NPARTS)) for i in range(NPARTS+1)]
for k in range(NPARTS):
    part = body[cuts[k]:cuts[k+1]]
    open(BUILD + r"\content_part%d.html" % (k+1), "w", encoding="utf-8").write(wrap(part))
# also keep a single-file version for reference
open(BUILD + r"\content_v4.html","w",encoding="utf-8").write(wrap(body))
print("wrote %d parts ; verses:" % NPARTS, len(V))
