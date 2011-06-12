#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# TODO: hyph-en, language parameter in blog entry, german exceptions?!
# TODO: less agressive, more xhtml conform 

""" Hyphenation, using Frank Liang's algorithm.

    This module provides a single function to hyphenate words.  hyphenate_word takes 
    a string (the word), and returns a list of parts that can be separated by hyphens.
    
    >>> hyphenate_word("hyphenation")
    ['hy', 'phen', 'ation']
    >>> hyphenate_word("supercalifragilisticexpialidocious")
    ['su', 'per', 'cal', 'ifrag', 'ilis', 'tic', 'ex', 'pi', 'ali', 'do', 'cious']
    >>> hyphenate_word("project")
    ['project']
    
    Ned Batchelder, July 2007.
    This Python code is in the public domain.
"""

import re

__version__ = '1.0.20070709'

class Hyphenator:
    def __init__(self, patterns, exceptions=''):
        self.tree = {}
        for pattern in patterns.split():
            self._insert_pattern(pattern)
    
        self.exceptions = {}
        for ex in exceptions.split():
            # Convert the hyphenated pattern into a point array for use later.
            self.exceptions[ex.replace('-', '')] = [0] + [ int(h == '-') for h in re.split(r"[a-z]", ex) ]
                
    def _insert_pattern(self, pattern):
        # Convert the a pattern like 'a1bc3d4' into a string of chars 'abcd'
        # and a list of points [ 1, 0, 3, 4 ].
        chars = re.sub('[0-9]', '', pattern)
        points = [ int(d or 0) for d in re.split(u"[.a-zäöüßçáâàéèêëíñôó]", pattern, flags=re.U) ]

        # Insert the pattern into the tree.  Each character finds a dict
        # another level down in the tree, and leaf nodes have the list of
        # points.
        t = self.tree
        for c in chars:
            if c not in t:
                t[c] = {}
            t = t[c]
        t[None] = points
        
    def hyphenate_word(self, word):
        """ Given a word, returns a list of pieces, broken at the possible
            hyphenation points.
        """
        # Short words aren't hyphenated.
        if len(word) <= 4:
            return [word]
        # If the word is an exception, get the stored points.
        if word.lower() in self.exceptions:
            points = self.exceptions[word.lower()]
        else:
            work = '.' + word.lower() + '.'
            points = [0] * (len(work)+1)
            for i in range(len(work)):
                t = self.tree
                for c in work[i:]:
                    if c in t:
                        t = t[c]
                        if None in t:
                            p = t[None]
                            for j in range(len(p)):
                                points[i+j] = max(points[i+j], p[j])
                    else:
                        break
            # No hyphens in the first two chars or the last two.
            points[1] = points[2] = points[-2] = points[-3] = 0

        # Examine the points to build the pieces list.
        pieces = ['']
        for c, p in zip(word, points[2:]):
            pieces[-1] += c
            if p % 2:
                pieces.append('')
        return pieces

# hyph-de.tex from July 2011
patterns = u"""
.ab1a .abi4 .ab3l .abo2 .ab3ol .ab1or .ack2 .ag4n .ag4r .ag2u .ai2s .akt2a 
.al3br .al2e .al5l4en .al4tei .alt3s .ampe4 .amt4s3 .an3d2 .anden6k .and4ri 
.ang2 .an3gli .angs4 .angst3 .an3s .an4si. .ans2p .ans2t .an4tag .an3th .apo1 
.aps2 .ari1e .ark2a .ar4m3ac .ar2sc .ar4t3ei .as3t .as4ta .at4h .au3d .au2f3 
.au4s3 .ausch3 .ax4 .äm3 .ät2s .be3erb .bei6ge. .be3ra .be3r2e .berg3a .ber6gab 
.ber4g3r .boge2 .bo4s3k .bu4ser .by4t .ch2 .dab4 .da2r1 .da4rin .darm1 .da4te. 
.da4tes .de2al .de1i .de4in. .de1o2 .de3r4en .de1s .des2e .de3sk .des2t .dien4e 
.do2mo .do1pe .dorf1 .dü1b .dys1 .ebe2r1 .ehe1i .ei3e2 .ei4na .einen6g .ei2sp 
.ei4st .ei4tr .eke2 .el2bi .elb3s .em3m2 .en1 .en4d3er .en5der. .en2d3r .end3s 
.enn2 .enns3 .en2t3 .en4tei .en4tr .er8brecht .er2da .er4dan .er4dar .er4dei 
.er4der .er1e .ere3c .erf4 .er1i .er8stein .er8stritt. .er8stritten. .er4zen4 
.es1p .es3ta .es5t4e .est2h .es3to .es5tr .et2s .eu1 .eu3g4 .eu3t .eve4r .ext4 
.fe2i .fer4no .fi3est .fi4le. .fi4len .fi2s .flug1 .for2t .fs4 .fu2sc .ga4t 
.gd2 .ge5nar .ge3ne .ge3r2a .ge3r2e .ge3u .gs4 .guss1 .hau2t1 .he2 .he3fe 
.her3an .he3ri .he6r5inn .ho4met .ia4 .im2a .ima4ge .im5m .in1 .in3e .ink4 
.inn2e .int6 .inu1 .ire3 .is2a .jor3 .ka2b5l .ka2i .kamp2 .ka4t3io .ki4e .kle2i 
.kopf1 .ks2 .kus2 .le4ar .li2f .li4tu .lo4g3in .lo3ver .lus4tr .ma3d .ma2i 
.ma3la .ma2st .md2 .me2e .mel2a .men8schl .men8schw .men3t4 .mi4t1 .mm2 .näs1c 
.ne4s .ni4e .nob4 .no4th .nus2 .oa3 .ob1a .obe2 .oper4 .or2a .ort2 .orts3e 
.oste2 .ost5end .os8ten8de .oste6re .ost3r .ozo4 .öd2 .pa4r1e .par3t4h .pf4 
.ph4 .poka2 .pro1 .ps2 .ram3s .reb3s2 .re3cha .rein4t .reli1 .reli3e .res6tr 
.ri2as .richt6e .ro4a .ro3m2a .rö2s1 .rü1b .rü6cker6 .sali3e .sch4 .se3ck 
.sen3s .ser2u .se2t1 .sha2 .sim3p4 .si4te .ski1e .spiege8lei .st4 .sto4re 
.sucher6 .tage4s .tal2e .tan4k3l .ta2to .te2e .te2f .te3no .te2s .te4st .th4 
.ti2a .tid1 .ti2s .ti5ta .tite4 .to4nin .to4pl .to2w .tri3es .tro2s .ts2 .tu3ri 
.uf2e2 .ufer1 .ul4mei .um3 .umo2 .un3a2 .un3d .un3e .un3g .uni4t .un3s .uns4t 
.ur1 .ur2i .urin4s .ur3o2m .uro2p .ur3s2 .ut2a .ut3r .übe4 .ve5n2e .vo4r .wah4l 
.wa2s .wei4ta .wi4e .wor2 .wort5en6 .wor8tend .wor4tu .xe3 .ya4l .za2s .zi2e 
.zin4st .zwe2 2aa a1ab aa2be aa1c aa2gr 4a1a2n 4a2ar aa2r1a aar3f4 aart4 aas5t 
aat4s3 a3au a1ä a1b 2aba ab1auf ab1ä ab2äu 1abd ab1eb abe1e abei1 ab1eil 2abel 
abe2la a3ber ab1erk ab1err ab1erz ab3esse 2abet 2abew 1abf 3abfi 1abg 1abh 2abi 
ab1ins ab1ir ab1it 1abk ab1l 1a2bla ab5lag 1a2blä 2able ab4le. ab3li ab4lo 
3a2blö a2blu 1abn a2bo. ab2of a2bon 2abor ab3r a3bra a4brä 2abrü 1abs 2abs. 
abs2a 2absar ab3s2i ab3sp abst4 2abst. ab3ste ab3sz 1abtei 2abu ab1ur 2abü 1abw 
2aby aby4t 1abz 2ac. 2aca 2ac1c a1cem 2ach. ach1a a1chal ach3au 2achb a1che 
a2ch1e2c ach1ei a4cherf a4cherk a4cherö a4ch3erw 4achf a1chi ach3l ach3m ach3n 
a1cho a3cho. ach1o2b ach1or ach3ö ach3r ach3su a4cht acht5erg ach2t1o ach8traum 
ach8träume. ach8träumen. ach6trit a1chu ach1u2f ach3ü 2achv 4ach1w a1ci ac1in 
a1ckar ack2en a2ckin ack2se ack3sl ack3sta4 a1cl acon4n 2acu a1ç a1d 2ada. 
a3d2ab ad2ag ad3ama a2d1an 3a4dap a3d2ar3 4adav 1a2dä ad1c 1add 2ade. ade2al 
adefi4 a2dein 2aden ade1r2a a2deri 4ade1s ade3s2p ades4s ade5str 2adf 2adh 
4a3di adi3en 5adj 2ado ad2ob 2adp 2adq 2ad3rec ad4res ad3ru 2ads2 ad3st ad3sz 
2ad2t1 ad4te ad4tr 2adu 2a1e ae2b ae2c ae2d a2ek a2ela a2ele ae2o3 ae2p 
3a2er2o1 aes5t a2et a2ew ae2x af1a a2fak a2fan a3far af4at a2fau 2afe a2f1ec 
a2fent af1erl a2fex af2fl af4flu 2afi 2af3l afo1s a2fö af3ra af3rä af3re af3rö 
af3s2a af2sp af2t1a af2tei af4t3erl af2t3r af4t5re af2tur a2f3ur a1g 2aga ag1ab 
ag1a2d ag1ar ag1au ag2di ag2dr ag2du age1i age4na age4neb a2gent a4gentu 
age4ral 2ages age2sa age4sel age4si age2s3p ag3esse age4s3ti ag3gl 1aggr 3a2git 
2a2gl ag4la a4glö ag2n ag4ne. ag4nu a2g3re a2g3ri ag4ro agsa2 ag4sam ag4set 
ags3p ag4spo ag3sta ag3ste ags4toc 2agt ag2th a2gund 2ah. 2a1ha ah4at 2a1he 
a2h1erh ahe1s a1h2i ahin3 ahl3a2 ah4l1ei ah4l3erh ah2lö ahl3sz ah4n1a ahner4e 
ahnt2 1ahor ah1os a2h3ö ahr1a ah3r2e ahre4s3 ah3ri ahrta4 ahr6tri 2ahs aht3s 
a1hu ah1w a1hy 2ai aian3 aid2s ai1e2 aien3 aif2 ai3g4 a3ik. ai3ke ai3ku a2il 
ai2lo a1ind ain4e a1ing ain3sp ai2sa a3isch. ai3s2e aiso2 a3iv. aive3 a3ivl 
a3ivs a1j aje2 2ak. 1a2k4ad 2akal 2a3kam 2akar ak4at 1a2kaz 2akb 2akc 2akd 
4a1ke a2kef aken2n a2keu 2a1ki 2ak3l ak4li 4ako 2a1kr 4akra ak3rau 3akro 2aks 
ak3sh 2akta ak5tan 2aktb 2aktik ak2t3r ak5t4ri 2aktst 2a1ku a2kun 4a3kü 1akz 
a1la 2ala. al1ab ala5ch2 al1af ala2g al1age a3lal al1am al3ame alami5 al3amp 
al1ana a2l1ang al1ans al1anz a2lar a3lar. a3lare al2arm al3arr ala4s al1asi 
al1ass 2alat al1au al3aug a1lä al1äm alb3ein alb3eis al4berh al4b3erw al2b1l 
alb3li al2boh al2br alb3ru alb3s al2dä al2dr alds2t al3du 2ale 3a2l1e2b 3a2l1ef 
a4l1eh a2l1ei a4l3ein a2l1el alen1 al3ends a2leng ale2p al1epo a2l1erf a2l1erh 
al1erl 3alerm a2l1ert 3a2lerz a2l1esk ale4t al1eta al1eth a2l1eu a4leur 3a2lex 
alf4r 3algi al2gli 2ali ali4ene ali4nal al1ins a2linv alk1ar 1alkoh alk3s2 
alks4t al2lab al2l3a4r al2lau al3lend all5erfa al3les alli5er. alli7ers. al2lob 
3almb 2alo a2l1o2b alo2ga al1ope al1orc a2l1ö al2ös 3alpe. 1alph al3skl al4spal 
al5s6terb al3sun al2tak al3tam alt3eig al4t3erf al2tre al2tri alt3ric al2tro 
alt2se alt4stü a1lu al2uf a2lum al1umb al1ur 4aly alzer4z al2zw 2am. 2am2a 
amab4 amad2 ama3g 2amä 2ambiq 2am4e 4ame. a2meb ame2n1 amer2a a2meri ame3ru 
a4mesh a3met a2mew 2amf a3mi. a3mie 2a3mir a3mis ami3ta ami3ti 2amk 2aml 2ammal 
am2mei am2min 2amml ammu2 a2mö amp2fa2 am3pr 2am2s am3sa am4schl am3str 1amt. 
am2t1a am2t1ä am4tel 2amtem am4t3ern am4tö am2t3r am4tre am2tu 2amu 2ana. 2anab 
ana3c anadi3 a3nak an1alg ana4lin 2anam 2anan 2ana1s4 an1äs 1anb 2anbu an3ch 
2and. an3dac and4art andel4s ande2s an2dex an2d3rü and4sas and6spas and3ste 
and2su 2andu and1ur 2ane an3e2c a3nee an2ei. an3eif an1e4k 3a4n1erb an1eth 1anf 
2anfi anft5s an3f2u 4ang. 3angeb an2g1ei an4g3erf an4g3erl an4g3erz 2angf 2angh 
2angie ang1l an2gla 2ango ang1r an2g3ra 4angs. ang4s3po 1anh 2a3ni an2id 
ani5ers. 3a4nim a4nins 2anj 2ank. an2k1an an2kei an3kl an4klö an2k3no ank1r 
an2k3ra an2k3rä ankt4 an2ky 1anl 2anmu 2ann 3an3na ann2ab 3annä an3n2e an1od 
a3nol a2n1or a3nos a1nö 2anpr 1anr 1ansä 1ansc ans2en an2seu 2ansk an3skr 
ans1pa 1anspr an3s2z 2ant. an2t3a4r 1antá 1antei 3antenn an3t4he 1anthr 2anto 
1antr ant3rin an2tro 1antw 2a1nu anu3s a1nü 1anw 2anwet 2anzb 1anzei 2anzg 
an2z1i4n 2anzs 1anzü 2anzw an2zwi 2ao ao1i a1op a1or a1os3 ao3t2 a3ot. a1ö a1p 
2ap. 2apa 2ape a2pef a3pel a2pé a2pf ap2fa a3pfl a3phä a2pht 2ap3l ap2n a2pot 
3appl ap3pu 2apr 2a3pu 2aq 2ar. a1ra a3ra. ar2ab ar3abt ara3d2 a2r3al a3ra3li 
a2r1ang a2r1ans a2r1anz a2r3app 2a2rar a2r1au a1rä 1arb 2arb. 4arba ar2bau 
ar2bec 2arben 2arbi ar2bl 2arbr ar2bre 2arbs2 2arbt 2arbu ar2b3un 1ar1c ar2dro 
2are a2rea ar1eff a4reg a2reh ar1ehr a2rein a4rek a3ren aren4se are3r2a ar2erf 
a2r1erh a2reri a2rerl are3u ar2ew 2arf arf1r ar2f3ra ar2gl ar2gn 2arh 2ari 
ar2ia ari3e4n ari3erd ari3erg ar1im arin3it ar1int a3riu ar2kal ark3amt ar2k1ar 
ark3aue ark3lag ar2kor ar4kri ark1s4 ark3sa ark3sh ark4tre ar2les arm2ä ar4merk 
ar3m2or ar2nan arn2e 2a1ro ar1ob a2r1o2d a2r1op a2ror 2arr ar2r3ad arre4n3 
ar2rh arr3he 2arsa ar4schl arse3 ar3s2h 2arsi ar2st ar3sta ar3t2e ar2the ar3t2i 
artin2 2arto art3r ar4tram ar6tri 2arts 2aru ar1uh ar1um a2rü 2arv arwa2 2ary 
ar2zä 2arze 1arzt ar2z1w as1ala as3au a2s1ä a2sca a3sche a4schec a3schi asch3la 
a2schm a3schu 4as2e a2seb a2s3e2m a3ses 4ash a3s2hi asin2g 2asis aska3s a3skop 
a2s1o2f as1or a2sö a2s1p as3pan as2ph as2pi as2po a3spu as3s2a as3s2e as4s3ei 
as3s2i as2s1p as2st ass3ti as3str as3stu 2as3ta a1s4tas as4tau as3te as2th 
as3ti as3to as4tof 2astr ast3rä as6t3re a2sü aswa2s 3a2syl a1ß aße2 aßen3 2a1t 
ata1 at1ab at2af at4ag a2t1akt ata3l a3tam at1apf at1au a2taus a2t1ä at2c at2e 
4ate. a2teb at3eig a2teli 4aten a2tep ater3s2 ate2ru 4ates at2h at3ha 4athe1 
3athl 4a3ti atil4s ati2st 3atm 4atmus ato4man 4ator a2t1ort at1ö 4atr atra4t 
at3rä at3re at3rom at2sa at4schn at2se at4set at2si at2so at2s1p at3ta at4tak 
att3ang at4tau at2tei at3t4hä at2t3rä att3s a3tub atu2n a3tü atz1er at4zerk 
at4zerw at2z1in at2zo atz3t2 at2z1w a2u 2au. 2au1a2 2aub au2bli au2blo 4auc 
auch3ta au2dr 2aue aue2b au5erein aue2s au2fa auf1an 2aufe. 2aufeh auf1er 
au4ferk auff4 3aufn 2aufs. 2aug 4augeh 4au1i au2is 2auj aule2s au3lü 4aum 
au2mal au2m1o aum3p2 aum3s6 4aun au3n4a aun2e au2nio au1nu a4unz au1o 2aup2 
aup4ter 2au3r2 au2s1ah ausan8ne. au2sau 2ausc au4schm au4scho 1ausd aus3erp 
au4s3erw 3ausf 1ausg 1ausl au2so au2spr 1ausr aus3s2 3aussag aus4se. auster6m 
aus5tri 1ausü 1ausz 2aut. au2t1äu 2aute au4ten4g au4t3erh 1auto 2auts4 2auu 
2auw 2aux 2auz auz2w 2a1ü 2a1v a3v4a ava3t4 4avi a2vr 2a1w awi3e a1x ax4am ax2e 
2a1ya a1yeu ays4 aysi1 ay3t 2a1z az2a az2o az2u ä1a ä1b ä2b3l äb2s ä1che äche1e 
ä1chi äch3l ä2chr äch2sp äch4st ä1chu ä1ck äck2e ä1d ä2da ä2d1ia ä2dr äd2s 2ä1e 
äf2fl äf3l äf3r äf2s äft4s3 ä1g äge1i äge3s ä2g3l äg2n ä2g3r äg4ra äg3str 1ä2gy 
äh1a 2ä3he ä3hi ähl1a ähl2e äh4l3e4be 2ähm äh3ne äh3ri 2ähs 2äh3t4 ä1hu äh1w 
ä1im ä1is. ä3isch. ä1isk ä1j ä1k ä2k3l ä2k3r ä1la älbe2 äl2bl 2äle äl2l1a äl2p3 
äl4schl ä1lu ämi3en 2äml äm2s ämt2e 2än. än5de än2dr 2äne äne2n1 äne1s än2f5 
2änge än2gl än2gr äng3se 2ä3ni änk2e än2k3l än2kr änk2s än3n4e2 2äns än2s1c 
änse3h ä1on ä1pa äp2pl äp2pr äp2s1c äp4st 1äq ä2r3a2 är4af är1ä är1c 4äre 
ä2r1ei äre2n ä2r1ene är2gr är1int är2k3l ärk2s är4ment ärm2s är1o2 ä1rö ärse2 
är4si är2st ärt4e är2th ärt2s3 ä2rü 1ärz är2zw ä5s4e äse3g2 äser4ei äse4ren 
äser2i äse3t äskop2 äskopf3 ä3s2kr ä2s1p äs6s1c äss2e äs4s3erk äs2st ä4s3t2 
äs4tr ä3su ä1ß äß1erk ä4t1a2 ä3te ät2e1i ätein2 äte2n ät2h ät1ob ä2t3r ät2sa 
ät2sä ät4schl ät4schr ät2s1i äts3l ät2s1p ät2s3t ät4tr ät2zw äu2br äu1c äude3 
äu3el ä2uf äuf2e 1äug äug3l 4äul 2äum äu2ma äum4s5 ä2un äun2e äu1nu 2äur 2ä3us. 
äu4schm äu3se ä3usg ä3usk ä3usn äu2sp äus2s1c 1äuß äu2tr 4ä1v 1äx ä1z â1t á1n 
ba2bl 2babs bach7t4e backs4 b1a2dr 2b1af 3bah bah2nu bais2 ba2ka ba2k1er ba2k1i 
bak1l bak1r ba2kra 3bal bal2a bal4l3eh bal6lerg bal3th 2b1am ban2a 3b2and 
ban2dr ba3n2e b1ang ban2k1a ban4kl ban2kr 2banl 2b1ans ban3t b1anz bar3b bar3de 
ba2rei bar2en bar3n bar3zw 3bas ba3s2a ba2sc ba2st bau3g bau1s bau3s2k bau3sp 
ba1yo 3b2ä1c b2är b2äs 4b1b b3be bben3 bbens2 bbe4p bb3ler bb2lö bbru2c bb2s 
bbu1 2b1c 2b3d4 bde1s 3be. 3bea be3an be3ar be3as 3beb b2ebe 1be1c be2del bedi4 
be1eh be2erk be1erl be1eta 3bef4 be3g2 2b1eier bei1f4 beik4 beil2 bei3la 
2b1eime b2ein be1ind be1in2h bei3sc beis2e bei1st beit2s 3bek 3bel be3las 
be3lec be3lei be2l1en be2let be3li bel3la bel3sz bel3t4 1bem 1ben. ben3ar 
ben3dor be3nei 3ben3g be3n2i ben3n ben2se ben4spa ben4spr benst4 ben2su 2bentb 
b2enti ben5t4r b1ents 2bentw ben3un ben3z2 be1o be1ra ber3am be2ran ber4ei. 
be4r3eiw be4rerk bere4s ber6gan. ber4in. ber3iss ber3na b1ernt be2rob be3rop 
ber3st4a be3rum 3be1s bes2a be2s1er be3slo bes2po bess4e b3esst. bes3sz 
be6stein be4s3tol be3s4ze 3bet be2tap be3tha be1ur 3b2ew 2b1ex 1bez 2b5f4 bfal2 
2b1g2 bge3 bges4 2b5h2 bhut2 1bi bi3ak bib2 bibe2 bien3s bie2s bik2a bi2ke. 
bi2kes 3bil bil2a bi2lau 4b1illu bi2lu 2b1inb bin2e 2b1inf bin3gl 2b1int bi2o1 
bio3d bi3on biri1 bi3se b1iso bi2sol bi2sp bis2s1c bi2s5t b2it. b2it2a b2ite 
bi2tu b2i3tus biz2 4b1j bjek4to 2b1k4 bl2 2bl. bla3b4 b3lad b2lanc 3blat b2latt 
2b3law b2le 3ble2a b3leb 2b3leg 2b3leid b3lein 3blem 3blen b3lese ble3sz b4let 
b3leu 2blich 3blick b2lie 2blig bling4 b3lis b2lit 3blitz b2lo b4loc b3los 
2blun 3blut 3blü 2b1m 4b3n2 bni2 bnis1 bo4a bo5as b1ob3 bo2bl bo2br bo2c bo3ch2 
bo3d2 boe1 bo2e3i 2b1of bo3fe bo1is bo2l1an 3bon. bond1 bon2de bo2ne 3bons b1op 
bo1r2a bo4rä bor2d1i bor2d3r bo2rei bo4rig bor2s b1ort bor2t3r bo2sc bo4s3p 
bote3n4e bo3th bot2st bo2xi bö2b3 2böf 2b1p2 bpa2g 2b1q b2r4 2br. b4ra. 2b3rad 
b4rah b4ra3k bra1st4 3brä brä4u 2bre. 3brea 6b5rechte 2b3ref 2breg b3reif 3brem 
2b3rep b4rer 2b3riem bri2er 2brig b4rio b3roh 2b3rol b4ron b4ruc bru4s brust3 
bru2th 3brü 4b1s b2s1ad b3sand bs3ar bsat2 b3sä b4sär bs2äu b5sc bs2ca b6schan 
b6schef bs4cu b3se. bse2b b3sel. bse2n1 b4s1erf bs3e4r3in b4s1ers b3s2es bsi4t 
bs2ku b4sl b2s1of bso2r b2sö bs2pl b3s2pu bss2 bs2t bst1a2b bst3ac bst1ak 
bs3tät bst3er b2stip b3sto b4stod b3stö b2s3trä bs3treu bs4tri b3stü b4stüb 
b2s1un 4b3t btal3 btast3r b5te b4th btil4 bt4r b4ts2 btü1 bu2chi bu2e3 bu2f 
bu3li bul2la 2b3umk bung4 b2urg bu3r4i bu2sa bu4s3cha bu4schl bu4schm bu4schw 
bus1er bu2sin bu2s1p bu2s1u bü1c bügel3e 2b1v 2b1w 3by1 by3p bys2 2b3z2 bzeit1 
1ca 2c1ab ca1ch ca2e3 ca3g4 ca1h cal3t 3cam c4an ca2pe 3car car3n carri1 
ca3s2a3 cas3t ca3t4h ca1y2 cä3 cäs2 2cc c1ce c1ch2 c2d2 c3do 2cec ce2dr 2cef 
ce1i 2cek 1cen cen3g 1cer cere3 ce3sh 1cet 2ceta ce1u 1cé 2c1f c4h 4ch. 2chab 
ch3a2bi cha2ck 2chaf 2ch1ak ch2anb 3chanc ch1ang ch3anst 4chanz 1chao 4char. 
1chara 3charta cha2sc 3chato 4chatu ch1ärm ch1äs 1châ 2chb 2chc 2chd ch3e4ben 
1chef 3chef. che4fer 3chefi 3chefs 4chei ch1eim 4chelem che4ler 4chents 4chentw 
cher3a che3rei 6chergeb cher6zie ch1ess 2cheta 2ch1e4x 1ché 2chf 2chg 2chh 
1ch1ia 2chic chi3na 4chind 3chines 2chinf 2chinh ch1ins ch1int 2ch1inv 1chiru 
2chj 2chk 2chl2 ch2le ch3lein ch2lu 4ch2m 2chn4 chner8ei. 2chob cho2f ch1off 
ch1oh ch1orc 2chp ch2r4 4chre chre3s ch3rh 1chron 4chs 2cht 2chuf 2chuh 2chum 
2ch1unf 2chunt 4chü 2chv 4chw 2chz ci1c ci2s c1j c4k 4ck. ck1a 1cka. 2ckac 
1ckag 2ckal 2ck3an cka4r1 2ckau ck1ä 2ckb 2ckc 2ckd 1cke 4ckeff 2ckeh ck1ehe 
4ck1ei 4ckense ck1ent 4ckentw cke2ra ck2ere 6ckergeb ck1erh 4ckerhö 4ckerke 
ck2ern 2ckero 2ck1err 4ckerze 2ck1ese 2ckex 2ckf 2ckg 2ckh 1cki 2ck1id ck1im 
ck1in 3ckis 2ckk 2ck3l 2ckm 2ck3n ck1o2 2ckp 2ck3r 4cks ck4stro 2ckt ckt2e 1cku 
2ck1um3 2ckunt 2ck1up 2ckv 2ckw 1cky 2ckz c4l2 clet4 clo1 1clu c2m2 3co co2c 
co3ch co2d2 co4der. co3di coff4 coi2 co1it co2ke co2le col2o com4te. comtes4 
con2ne co2pe co1ra cor3d co3re cos4 co4te cô4 2cp 2c1q 1c4r2 cre2 cre4mes cry2 
2cs cs2a c2si c1s4tr 4c1t cte3e cti2 cti4o ctur6 3cu cu2p3 cussi4 1cy 2c1z 3da. 
da1a 2d1ab 3d2abä da2ben 3d2abl da2bre dab4rü 2d1ac dach3a da2cho dach1s 
4d3achse d1af d1ag dagi2 dah3l da1ho 3d4ai da1in da1is dal2a 2d1alar dal3b2 
da3lö d1alt d1amma 2d1ammä damo3 d4amp dampf8erf 2d1amt d2an. 2d1ana dan4ce. 
2d1an3d2 d1ang 2dange dan4kl dan5kla dan2k1o dan2kr 2d1ans 2dantw 2danw d2anz. 
4danzi 2d1ap d2aph 4dapp da2r3a 2darb2 3d2arl dar2ma dar2m1i da2ro d3arr d2ar3s 
d1art da2ru d2arw da1s da3s2h das4t dat2a dat4e2 da3tei date4n 4d3atl 4datm 
dau3e 2d1au2f 2dauk 2d1aus3 4daush 2d1äh 2d1ämt 2d1änd 2d1äng 2d1äp 2därz dä2u 
dä3us 2d1b4 dbu2c 2dc d1ch dco4r 2d1d2 ddar2 d3dh d5do 1de de2ad de3as de3a2t 
de3b4 2d1e4ben 3de1c de4ca. de2cka deco3 de1e4 2d1eff deg2 de3gl dehe2 de3ho 
2d1ehr d1ei d2eic 3d2e1im dein2d dein2s de2l1a4g de4l3aug del1än del1ec delei4g 
de3lein 2delek 2delem 2delfm delle2 del4leb del4lei de2l1ob de2lop de3lor de2lö 
del4san del5sc del2s5e del2so del2s1p del5ster del3t4 dem2ar 2d1emp d2en. dend2 
de4n3end 4denerg den3g d2enh de2ni den4k3li 4den4sem den4sen den6s5tau den3th 
2dentw de1nu de1on depi2 d4er. dera2b de1rad de2rap der2bl 2derdb de2re2b 
de4reck der3edi derer3 de3r4erb de3r4erf de4r3ero derer4t 4d3erhöh 3derie 
derin4f 4derklä der3m2 4derneu 4d3ersat der3tau der6t5en6d de3ru de4ruh de4rum 
des1 de2sa de3sac desa4g de4sam des2äc de2seb de4seh de2sei des3elt de2sen1 
de4set de2sin de2sor de2sp des3s2 dest5alt de2sto dest5rat de4stre des4tum 
de2su det2 deten4t 2d1etw de1un de1url de3us de2xis 2dexp 2d1f4 2d1g2 dga2 
d2ge. dge4t1e d3gl 2d1h2 dha1s4 d2his 1di di4ab di2ad di4am 3dic di1ce di2e 
di3e2d die4neb di3eni di3ens. die2s3c diet3 die2th dige4s dik2a dil2s5 2d1imb 
din2a 2d1ind 2d1inf 2d1inh 2d1in1it 4d3inner 2d1ins 2d1int di2ob dion3s di1p 
di4re. di2ren di2ris 2d1irl di2sp 2d1isr dist2 di2s5te di2ta di4teng di4t3erl 
di4t3erm di4t3ers di2th di4t3r dit3s di2tu di5v di3z2 2d1j 2d1k4 4d1l2 d3la 
d3le dle2ra dli2f dl3m dl3s 2d3m2 4d5n2 dni2 dnis1 d1ob d2oba 2dobe dob4l d2obr 
2d1o2f dole4 doll2 do2mar do5n4a doni1e do2o 2dope 2d1opf d2opp d2o3r4a 2dorc 
2dord dor2f1a dor2fä dor2fl dor2fr 2d1org do2rie d2orp 2dort dor2ta d2os. dos3s 
dost1r dot6h do3un d1ö dö2l1 3d2ör dö2s1c 2d3p2 2d1q d2r4 3d4ra. 2d3rad drag4 
2drahm d3rai 3d4ram d3rand 2d3rast 2d3rauc 2dräd d4räh 2d3rät 2d3räu 4dre. 
d4rea. d4reas 3d4reck 2dreg 3d4reh 2d3reic d4reiv 4drem 4d3ren 2d3rep 4d3rer 
4dres. d4resc 2d3rh d3ri d4ri. 3d4ria 2d5ric d4rid d4rie d5rieg d4rif d4rik 
d4ril d4rin. 3d4risc 3d4rit 4dritu d3rob d3roc 2d3rod d4roi 2d3rot d3rou 2d3rov 
d3rö drö2s1 d5rub 3d4ruc 2d3ruh drunge3 2d5rut drü1b drü5cke 2d1s d4s1amt d2san 
ds3assi d2sau2 ds1än 4dsb d4schin d2s1e2b d2s1ef d3sei ds2eig d4seins d2s1eng 
d2s1ent d2s1erf d2serh d2s1erk ds1err d2s1erz dse4t d4s1eta d3s2ha d3sho d2s1im 
ds2inf d3s2kan d3skul 4dsl d2s1op dso2r ds1ori d2sö d2s1par ds1pas d2spä ds2po 
d2spro ds2pu dss4 dst4 ds3tab d4stag d4s3täti d2ste d4stea d3stei d3stell 
d4stem d3s4tern ds2ti ds4til ds4tip ds2tu ds1ums d2sun ds2zen 2d1t dta2d d5tea 
d2th d4thei dt3ho dto2 d3tö dt3r dtran2 dt5s2 d3tü 1du du1alv du1ar dub3l 
du2bli du2f 2d1ufe 2d1uh du1i 2d1umb 2dumd 2d1u2m1e 2dumf 2dumg 2d3umk 2duml 
d2ump 2dumr d1ums d2ums. 2d1umv 2d1un3d dund2a 2d1unf dung4 dun3ke dun2kl 2dunr 
dun2s 2dunt du1o dur2 2d1url 2dursa du4schn du4schr du4schw dus3t 2düb 3düf 
3dün 2d1v2 2d1w dwa2 dwest3 dy2s 2d1z 2e1a e3a2b eab3l ea2c ea3der eadli4 ea2dr 
ea2g4 ea3ga ea4ge ea3gl eak1 eakt2 ea2la e3alei e4aler. eam3 eam1o ea2na e2ano 
e3ar. ea2ra e3a4rene e3arr e3arv e2as eas3s eat4e2 eater1 e3ath ea5tr eat3s2 
e3at5t4 e3au2f e3aug eau1st e1ä2 e1b 2eba e3b2ak 2ebed ebe2i 2ebel eb2en 
ebens3e 2ebet 2ebl eb3ler eb4leu e3blie eb3lo eb2lö 2eb2o ebot2 ebö2s 2ebr 
eb3rei eb4ru eb2s1 eb6sche ebse2 ebs3pa eb3sta eb4stät ebs3tem ebs3t2h eb3str 
e3bu ebu2t1 2e3ca e1ce ech1ä 2e3che ech1ei e6ch5erzi e1chi ech3l ech3m ech3n 
e2cho. ech1o2b e2ch3r ech3ta ech3t4ei e1chu ech1uh ech1w e1ci eci6a eck3se 
2eckt 2e1cl 2eco e3cr ec1s4 2ect e1d e3d2a ed2dr ed2e ede2al e3dei ede3n2e 
edens1 eden4se eden4sp ede2r eder3t2 edi4al e3d2o ed2ö eds2ä ed2s1es ed2s1o 
ed2s1p ed2s3tr ed2su edu2s e3dy3 4ee ee3a2 eeb2l ee2ce ee1ch ee2cho ee2ck eede3 
eed3s2 ee1e e1eff eef4l eef3s eeg2 e1ei ee1im eein4se eel2e ee2lek ee3len e1emp 
e1en eena2 ee4nag e2enä e2enc ee3ni e2eno een3s e1e2pi ee1ra e1erbt e1erd 
ee3r2e ee4r3en4g eere2s ee4ret e1erk ee1rö eer2ös eert2 e1ertr ee3r2u e1erz 
ee3s2 ees3k ee3ta ee4tat ee2th ee1u2 eewa4r e1e2x e1f 2ef. 2efa e2f1ad ef1ana 
ef1ar e2fat e2fäu 2efe e3fe. e2f1e2b ef1em e2fent ef2er 2eff. 1effi ef2fl 2efi 
e2f1i2d e2f1ins efi2s 1efku 2efl e3f4lu 2e3f2o e3fra ef3rea ef3rol ef3rom ef4rü 
efs2 ef3so ef3sp ef2tan 2efu e2fum 2efü e1g egas3 egd4 e3ge ege4n3a4 ege2ra 
ege4str ege1u e2glo e2gn eg3ni eg4sal eg4se4r1 eg4sto eg2th 2egu egung4 egus3 
2e1ha eh1ach e3h2al eh2aus 2e1hä e1he eh2ec eh1eff eh2el ehen6t3 1e2hep e3her 
ehe1ra ehe3str e1hi eh1int eh1lam eh1lä ehle2 ehl3ein eh4lent eh5l2er eh2lin 
eh3lo ehl2se 2ehm eh3mu e1ho e3hol ehr1a2 ehr1ä ehr1e2c eh2rei ehr3erl ehr6erle 
ehre3s eh3ri eh1ro2 ehr1ob ehr1of ehs2 eh3sh eh1ste 2eht e1hu e2hunt e1hü eh3üb 
eh1w e1hy 2ei3a2 4eib ei2bar ei2bl eibu4t ei4b3ute ei2cho e2id ei2d1a ei3dan 
ei3de ei4d3err 2eidn ei3dra ei1e 4eien3 eienge4 1eifr ei3g2a 4eigeno eig2er 
2eigew ei3gl 1ei2g3n 2eigru 2eigt 2eigu eik2ar ei3kau eik4la e4il 2eil. ei2lar 
ei2lau 2eilb eil3d ei4lein eilen1 eil3f4 eil3ins 2eiln 1eilzu ei2m1a4g eim3all 
ei2mor e1imp eim2pl ei2n1a ei4nas ei4nä ein3dr 2eindu ei4neng ei2neu 2einfo 
ein4fo. ein4fos ein3g2 ein4hab e1init ein3k ein6karn 3einkom ei2n1o2 3einsat 
ein6stal ein4sz e4inver ei3o2 ei1p eip2f 2eir ei3re e1irr e2is. ei2sa4 ei6schwu 
ei4s3erw eis2pe eis4th ei1sto ei2sum e2it ei2tab ei2tan ei2tar 2eitä ei3te 
ei2th ei2tro eitt4 eit3um 2eiu 2e1j e1k ek2a 1ekd e3ke. e3ken e3kes e3key e3k2l 
ek4n ek2o ek4r ek1s4t 2ekt ekt4ant ekt3erf ekt3erg ek4t3erz ekt2o ek5tri ek2u 
e3k2w e1la ela4ben el2abt ela2c el1af ela2h e2l1ak e2l3a2m el4ami el4amp el1ans 
el1anz 2elao e2l1ap e2l1a2r el3ari ela4s el1asi el1asp el2ast 2e1lä 3elbis 
el2da eld5erst el4d3erw eld3s2 2ele. elea2 ele2c 2eleh 2elei e6l5eier. e2l1ein 
e3leine e4leing 1elek e2l1el 1e2lem e3lem. el1emp 2e3len. e4lense e2l1ent e3lep 
el1erd el1erf e4ler4fa e2l1erg el1erk el1erl e4ler4la e4l3ernä e2l1err 2eles2 
el1ess e4l1e4ta e3leu 2elev ele2x 1elf. el3fe elf4l 1elfm 1elft elgi5er. 
elgi5ers 2eli e2l1id e3lie eli2ne el1ita el3kl el3lan el3le el5le. ell3ebe 
el4l3ein ell3eis el3lin ell3sp elm2a 2eln el5na 2elo e2lof e2lol elon2 el1ope 
e2l1or elo2ri el2öf elö2s el2sum elte2k elt3eng 3eltern elto2 el2t3r elt3s2k 
elt3s2p 2e1lu e2l1um el1ur el3use e1lü e2lya 2elz elz2e el2zwa e1m 2ema e2m1ad 
ema2k e2m3anf e2m1ans 3emanz em2d3a2 e3m2en emen4t3h e6mentsp e2m1erw eme2s 
1e2meti e2m1im em1int emi3ti 2emm emma3u em2mei e2mop 3empf em3pfl em2p3le 
em2sa em2spr em2st em3t2 1emul 2emü e2n1a 4ena. 2enac e3nad e4naf 4enah e4nak 
ena3l2i 4enam en4ame e4nand en3ang en3are en2asc 4enat en3att e3naue e2n1är 
en1äu en4ce. en3d2ac en2dal en4d3ess end4ort end3rom end3si end3s2p end3sz 
end2um 2ene. ene4ben en1e2c e2neff e4nein e2n1el ene4le 2enem 2enen e4n1ent 
en4entr 4e3ner. e2n1erd e2nerf 1e2nerg e4nerh e4nerk e2n1erl e4n3ermo 4enern 
e2n1err e2n1ers e2n1ert e2n3eru e2n1erw e4nerz 2enes e4n3ess en3f enf2a enf2u 
1engad 3engag en3ge en3g2i en2gl en3glo 1engp eng3se e3ni. e3nic e4nid e3nie 
eni3er. eni5ers. e2n1i4m e2n1in e3nio 2enis eni3se e3nit 2eniv en3k2ü e2n1o2b 
enob4le e2nof en1oh e3nol eno2ma en1on e2n1op e2n1o2r enost3 e3not eno2w 2e1nö 
en1ö2d e4nr en3sac en2sau en5sch4e en2seb ens2el 1ensem ensen1 en3ska en3s2po 
enst5alt en4s3tät 2ensto e4nt ent4ag 1entd en2teb en4terb 1entfa 3entga en2thi 
3entla 1entn en4t3rol 3entspr 2entü 1entw 4entwet 1entz en1u 2enut e1nü enü1st 
4enwü e1ny en4z3erf en4z3erg en4z3erk enz3ert e1ñ 2eo e1o2b1 e1of eo2fe e1oh 
e4ol e1on. e1ond e1onf e1onl e1onr e1ons e1ope e1opf eop4t e1or e3or. e3orb 
e3ors e3orw eo1s2 e3os. eo3ul e1ov e1ö2 e1p e3pa epa2g e3p2f4 1episo ep3le 
1e2poc ep2pa ep4pl ep2pr ept2a ep2tal e3pu epu2s e1q er1a e3ra. e3rad. er3adm 
eraf4a era1fr era2g e1rai er3aic e2rak e1ral er3all eran3d e3rane er3anf e2ranh 
er3anm e1rap er3apf e2rar e3rari e1ras e2r3a4si era2ß e2rath e3rati e2ratm 
e1raub er3aue erau2f er3aug e1raw e1raz e1rä er1äh er1äm erb2e er3br erb4sp 
er1c er3chl er3da 1erdb er3de 2erdec erd3erw 4ere. er1eb e3rech er3echs er1e2ck 
ere4dit er1eff e2r1e2h 4e3rei. er1eig e2rein e4r3eis. ere2l er1ele 2e3rem 2eren 
4e3ren. e3rena e4rense e4r3entf e4rentn e3renz eren8z7end 2erer 4erer. e2r3erf 
e2r1erh e4rerl 4erern e3rero er1err er1ers e2rert er1erw 2eres er1ess er3e4ti 
er1eul ere4vid erf2e erf4r 4erfür 3ergebn 4ergehä erg3el4s3 1ergol erg3s ergs4t 
er3h 1erhab 2erhü 2eri e2riat e3rib 4e3ric 4e3rie eri3e4n3 e3ri3k4 4e3rin. 
er1inb e2r1ini er1ink er1int e3rio er1ita 2erk. 1erklä 2erkre erk3t 3erlebn 
ermen4s erm3ers ern1os e1ro e3ro. er3oa er1o2b er1of er1oh e3ron e2r1o2p e4ro2r 
e3ros e3row er1ö erö2d 2erök er3p4 er3rä 2errü ers2a er3se ers2i er3sk er3smo 
er3sn er3sp er3sz ert2ak er6terei er4ters er2tho 4erti ert3ins ert4ra erts2e 
2eru eruf4s er1u4m er1und erung4 er1uns er3uz erü4b 3erweck 6erweis es3ab 
es2ach es3ak es3anz e3s2as e4s3ato 2esb es2c es3cap e3sce esch2 e3scha e2s3ein 
es2el ese4ler es3eva 2esf 4esh es2har es2hu es2id e2sil es3int es2ir es2kat 
e4ske es3kl es3ku e4sky es3l es4log 2esm es2ort e3sot es2ö 2esp e3s2pek e3spi 
e3s2por e3s4pra 2esr es2sau es3sc es3se 4essem ess4e3re ess3erg 2esso es2sof 
es2s1pa es2spu es3str es3stu estab4b est1ak e1star e4starb 1e2stas e1stat 
e1s2tec e3stel es4t3eng es4t3erh es4t3ess e1stil e2stip estmo6de est3ori e1str 
es4tri es3trop e1stu es4tü e2s1um es3ums es3w e3sy es3z e1ß eße3r2e e1t etab4 
et1am 3etap et4at et1äh e3te e4tein et2en eten3d2 ete2o eter4hö eter4tr et2h 
et3hal et3hü e3ti eti2m eti2ta 2e3to eto2b e4t1of etons4 e3tö 2etr e4traum 
e6t3rec e2tres et4rig etsch3w ets2p et3su ett1a et2tab et2t3au et2tei ette4n1 
et2th et2t3r et4tro ett3sz et4t1um e3tü etwa4r 2etz et2zä et4z3ent etze4s et2zw 
eu1a2 eu3erei eue6reif eu2esc eu2ga eu4gent eu3g2er eu4gla eugs4 euil4 eu1in 
1euk eu2kä e1um e3um. e3umb e3uml e3um2s eum4sc eums1p eum3st 2eun eun2e eu4nei 
e3un2g eu2nio eun3ka eu1o2 eu1p eur2e 3eu3ro eu3sp eust4 eu1sta eu1sto eu1str 
2eut eut2h eut6schn 2eux eu2zw e3ü 2e1v e2vela e2vent 4ever eve5r2i e3vo e1w 
2ewa e3wä ewä2s 2ewe e2we. ewinde3 e3wir ewi2s e3wit ew2s 2ex. ex3at 1e2xem 
ex1er e1xi e2x1in 1exis ex3l 3exp 2ext. ex2tin ex2tu 2exu 2e3xy ey1 ey4n eys4 
e1z e3z2a e2z1enn e3zi ezi2s ez2w é1b é1c é1g égi2 é1h é1l élu2 é1o é1p é1r é1s 
é1t2 é1u2 é1v é1z2 è1c è1m è1n è1r ê1p ê4t 1fa fab4 f1abe fa2ben fab5s 3fac 
fa4cheb facher5f fa2ch1i fa2cho f1ader fa2dr f4ah faib4 fa2ke f2al fa3l2a 
fal2kl fal6l5erk fal6scha fal6schm fal3te falt2s 2fanb 2fanf fan2gr 2f1ank 
2fanl f1anp 2fanr fan3s 2fanw f1an3z 2f1ap f2ar far2br 2f3arc 3fari farr3s 
3f4art 2f3arz fa3s4a fa3sh f3at fa2to3 2f1auf f3aug f1ausb 3f4av fa2xa 1fä fä1c 
fäh2r1u 2f1ärm fä2ßer f1äu 2f1b2 2f1c 2f3d4 fdie2 1fe featu4 fe2c f2ech 2f1eck 
fe2dr fe2ei fe1em fef4l feh4lei f4eie 2f1eing 4f1einh fe1ini 2f1einw f1eis 
fek2ta fe2l1a fel2dr 2fe2lek fe2l1er fe2les fe2l1o fel4soh fel3t f2em. fem4m 
2femp fe2nä fen3g fe2no fen3sa f1ent f2er. fe1ra fer2an fe4rang fe4r3anz fe2rau 
ferde3 f2ere fer2er fer3erz f1erfa f2erl. 4ferneu f4erpa f2ers. f2ert f1erw 
fe2st fest1a fest3ei 2f1e4ta 3fete fet2t3a feuer3e feu4ru 3few f1ex 2fexp 3fez 
1fé 2f1f ff3ar ff1au ff2e ffe2e f2f3ef ff3ei ffe1in ffe2m f2f3emi ff4en f2fex 
fff4 ff3l ff4la ff4lä ff4lo f3flu f3flü f3f4rä ff3ro ff3rö ff2s ff3sho ffs3t 
ffs4tr 4f3g2 fge3s 2f1h2 1fi 3fi. fi3at fid2 fi4ds fid3sc fien3 fi1er2f fi2kin 
fi3kl fik1o2 fi2kob fi2kr fi2l1an fil4auf fil3d fi2les filg4 fi3li fi4lin 
fil2ip f2ina fi3ni fin2s fin3sp 2f1int fi2o fi3ol fi2r fi3ra 3fis fis2a fisch3o 
fis2p fi2s5t fit1o2 fi2tor fi3tu 3fiz 2f1j 4f1k4 f2l2 2fl. f3lad f3lap 1flä 
3f4läc 2f5läd f3län 2f3läu 2f3leb f4lee 2f3lein f3ler f4lé f3li. 3f6lim fli4ne 
2f5lon 1f4lop 1f4lot flo2w f3lö f4luc 1f4lug flu4ger f4lü 2f3m2 2f3n2 fni2s 1fo 
fob2l 2f1of foli3 fo2na fo2nu 2f1op fo1ra 4f3org fo3rin 3form for4m3a4g 
forni7er. for4st for4tei for2th for2t3r for3tu 2f1o2x 1fö 2föf 2f1ök 2f1öl 
för2s 4f1p2 2f1q f2r2 f4rac frach6tr f5rad fra4m f3rand f5rap 1f4rän 2fre. 
f3rec f3red 2freg freik2 frein4 f3rep f4reu 2f3ric fri3d fri2e 2frig 1fris 
f4risc f3roc 1f4ron fro2na fro2s f3rot f3ru f3rü 4f1s fs1all fs4amm f2san fs3ar 
f2s1as f2sauf f2saus f2saut f3sc f4sce f4schan f4schef fs4co fs1e2b f4s1ehr 
f2s1em f2s1ent f2s1er fse4t f4s1eta f3si f2si2d f3s2kie f2s1o2 f3span f2s1pas 
fs1pen f2sph f3s2pl f3s2por fs1pr f2spre fs2pri f2spro fs2pru fs3s4 fs2t f2stas 
f4s3täti f4stech f3stei f3s4tel f3stern fs3th f2stip f3st4r f4s3tres f4s3tüte 
f2s1un f2sü f3sy 4f1t f4ta. f2tab ft1a2be ft1af f2t1al ft1an ft1ar f3tat ft1e2h 
ft1eig ft1eis f4t1ent f4t1e4ti f2th f4thei ft3ho ft1op f3tö f2t3ro f2t3rö 
f3t4ru ft2s1 ftsa4 ft4sam ft3s2c ft4sche ftse4 ft4seh fts3el ft3st ft4s3tan 
ft4s3tä fts2ti ft4stri f2tum ft1url f3tü ftwa4 ft3z2 1fu 3fug 3f2uh f1um 2f1unf 
fung4 2f1u2ni fun2kl fun2ko fun2k3r 2f1unm 2funt f2ur fu4re. fus2sa fus2s1p 
fus2st fu2ß1er 3fut 1fü 2füb fü2r 2f1v 2f1w 1fy 2f1z fz2a fzeiten6 fzei8tend 
fz2ö fzu3 fzu4ga 3ga. 2gabf ga2b5l gab4r 2gabz ga1c 2gadl 2ga2dr ga1fl ga3ge 
5gai ga1k ga2ka gal2a g4amo 2g1amt 2ganb gan3d gan2g1a 4gangeb gan2gr 2ganh 
2g3anku 2ganl g3anla 3g2ano 2ganw ga1ny 2garb 2garc 3gard 2g1arm ga3r2o g1arti 
ga3ru 2g1arz ga2sa gas3ei ga2si ga2sor ga3sp ga4spe ga4spr gas3s gas4ta gas5tan 
ga4ste gas4t3el gat2a 2gatm gat4r gau1c 2g1auf g2auk g1aus 2g1aut 2g1äp 2gärz 
gäs5 gä4u 2g1b2 gber2 gbi2 gby4t 2g1c 2gd g1da g2d1au g2d1er gd1in g1do g1dö 
g1d3r gd3s2 gdt4 gd1u 1ge ge3a2 geb2a gebe4am geb4r ge1c ged4 ge1e2 ge3ec ge2es 
gef4 ge3g2l ge1im ge2in. gein2s ge2int gein2v ge1ir ge2is 2g1eise2 gei3sh g2el 
ge4lanz gelb1r gel4b3ra gel6ders ge3le ge5leh ge4l3ers ge4less gell2a ge3lor 
gels2t gel3ste gel3sz gel3t2a ge3lum ge3lü gelz2 ge3mi gem2u 3gen ge3na ge4nam 
ge4nar gen4aug gen2d1r gen1eb ge3nec gen3eid gen3ern gen3g gen3n gen4sam gen3sz 
2g1entf gen3th 4gentw geo2r ge1ou ge3p4 ge1ra ge2rab 4g3ereig ge4reng ge4ren4s 
ge4r3ent ger2er gerin4f ger4inn gerin4t germ4 ger3no ge1r2ö ger4sto ge3r2u 
g2e1s2 ges3auf ge3sc ges3elt ge2s3er ge3si ges4pi ges3s2t gest2 ge3ste ge4s3ter 
ges3th ge3t2a 2getap ge5tr ge3t4u ge1ul ge1ur 2g1ex 2g1f4 4g1g gga4t g3ge 
gge2ne g2g3l gg4lo g2g3n gg4r 2g1h 4gh. gh2e 3g2het 3g2hie gh1l 3gh2r g2hu gh1w 
gi3alo gie3g gi2e1i gi2el gien2e1 gie1st gi2gu gi2me. gi4mes gi2met 2g1ind 
gi3ne gin2ga 2g1ins 2g3isel gi3t2a gi3tu gi4us 2g1j 4g3k2 4gl. g1lab g1lac 
3glad g2lade 2g1lag 3glanz 3g2laub 2g1lauf 3glät 2gläuf g2l4e 2gle. 3glea 
2g3leb g3lec g3leg 2gleh 4g3lein glei4t5r g3len 4g5ler 2gles g3lese g4lia 2glib 
3g2lid 3g2lie 2glif g2lik 4glin g2lio 2glis 4g3lisc 3g2lit g2liz 3g2loa 3g2lob 
g3loch glo3g 3g4lok g2lom 3g2lop 3g2lot 2gls 2g1lu glu2t 3glü g2ly 2g1m2 g1n 
2gn. g2n2a g4na. 2gnac g4nat 3g2nä gn2e g3neh gne2tr 2gneu 2gng g2nie g2nif 
g4nin 2gni2s1 3g2no gno1r 4g3not 2gnp 2gns 2gnt 2gnu 3g2num. g2nü g2ny 2gnz 
go4a goa3li 2g1of 2gog 2g1oh go1i gol2a 2gonis 2g1ope 2g1opf g2o1ra 2gord 2gorg 
go2s1 go3st go3th got6t5erg go1y 2g1p2 2g1q g2r4 gra2bi gra2bl 2gradl 2g3rah 
2g3rak grammen6 gram8m7end 2g3räu 2g5re. g4reb 2g3rec 2g3rede g4re2e 2g3reic 
2g3rein g3reit g4rem 2g3renn gren6z5ei g4rer g3ret g3rev 2g3ric gri2e g3riese 
3grif 2grig 2g3ring 2groc 2groh gron4 g4ros gros6sel gro4u 2g3röh g4ruf 2g3rui 
2g3rum 3g4runs 3g4rup 2grut 2g3rüc 3g4rün 4g2s1 gsa4g g3s2ah g4s3a2k g3sal 
g4salt gs3ama gs3an gs3ar gs3aug g3s2c g4sca g4s3ce gsch4 g4schef gs4chi g4sco 
g4s3cr gse2 gs2eh g3s2eil g3sel. gs3eli g3seln gsen1 gs3er gs5erk gse4t g4seta 
gsi2d g3sil g4sl gso2 gsp4 g3s2pek g3spi gs4pie g4spin gs2pit gs3pl g3s2por 
gsrat4 gsrü2 gs5s4 gs3ta g3stan g3star g3s4tati g4s3tä g5stäm g3stel gst3ent 
gst3err g1steu gst2he g3stir g3sto gs3toc g4stol gs3top g4s3tor g3stö gs3tr 
gst4ra gs4trat gst4ri gs4t3ros g3stu g4stur gs3tü gs4tüc g4sw g3sy 2g1t g3te 
gti2m gt4r gt2s g3tü 1gu gu3am gu1an. gu1ant gu1c gu2e 2gued guet4 2g1u2f 2g1uh 
gu1ins gu1is 3gumm 2g1unf g2ung. gunge2 4gungew 2g1ungl g2un4s 2gunt2 2g1url 
gurt3s gu2s3a guschi5 gus4ser gus2sp gus2st gu4st gu2t gut1a gu4t3erh gut3h 
2güb gür1 güs3 2g1v 2g1w 2g3z2 3haa hab2a hab2e h2abs ha2cho ha2del ha4din 
h1adle haf3f4l haft4s3p h1ah ha1kl 2h2al. halan4c ha2lau hal2ba hal4bei halb3r 
2hale hal2la hal6lerf h1alp hal2st hal4t3r h1amt h2an. h2and hand3s h4ann 2hanr 
2hant h1ap ha2pl ha2pr h4a3ra 2harb h2ard h1arm. har4me. har4mes har2th h1arti 
h2as 2ha3sa hasi1 hat5t2 hau3f4li 2h1aufm h1aukt hau2sa hau2sc hau4spa hau5stei 
hau6terk 2hauto hau2tr h1äff hä6s5chen häu2s1c hä3usp 2h3b2 hba2r3a 2h1c 2h3d4 
hdan2 2hea he2ad he3be he4b1ei he2bl he3br he5ch2e he1cho h1echt he3cke hed2g 
he3di he2e3l hee4s he2fan he2fä he2f1ei hef3erm 2heff he4f3ing he2f3l he2fr 
he3fri he2fu he3gu h1eie h1eif h1eig he2im heim3p hei4mu heine2 hei4neh h1eink 
4heio he1ism he1ist heit4s3 h1eiw he2l3au hel1ec h3e2lek he3len hel3ers he3li 
hel4l3au hel4mei he3lo he4lof he2lö 3hemd he3mi 3hemm 4h1emp h2en. he4n3a4 
he2nä hend2s he2n1e2b hen3end hen3erg he2net heng2 2heni he2no henst2 hen5tr 
h1ents 2h3entw hen3z 4he2o he3on he3op he3ph her3a2b he2ral 2herap he3ras 
herb4s he4reck 4hereig he4r3eis he2rel he4rerw h1er2fo h1erfü herg2 herin4f 
he6rin6nu herin4s herin8ter h1erke h3erlau 2herm he3ro he4r3o4b h1erö hert2 
her3th her2zw he1sta he2s5tr he2tap heter2 he3th het2i he3t4s h2e2u heu3g he3x 
he1x4a he1y2 1hè 2h3f4 hfell1 hfel6ler hfi2s 2h3g2 hget4 2h1h2 2hi. 2hia hi2ac 
hi2ang hi1ce hich6ter 2hi3d h2ide h1i4di hi2e hi3ens hier1i hie4rin hiers2 
hif3f4r hi2kr hi2l3a4 hil2fr hi2n h1indu hi3nel hin2en h1inf h1inh hi3n2i 
hin3n2 hi3no hin3s2 hin4t1a 2hio hi4on hi3or 2hip1 hi2ph hi2pi h2i2r hi3ra 
2hi3re hi3ri hirn1 hir4ner hi3ro hir2s his2a hi2se his2p hi2st hi1th hi3ti 2hiu 
h1j 2h1k4 2hl h4lac hla2n hl1anz h1las h1lat h1laut h3läd h1läs h1läu hlb4 hld4 
h3leb hle3e h5len. hlen3g hl2enn h3ler hle2ra hl1erg h6l3ernä hle3run hl1erw 
h4lerz h3les h4lesi h3lex hlg4 h2lie h2lif hl1ind h2lip h2lis h3list h2lit hll2 
hlm2 h2lo h3loc hl1of hl1op h4lor hlo2re h3losi hl2ö h3löc h2lös hl2san hl2ser 
hl3sku hl3slo hl3t2 h3luf h3luk h1lüf 2h1m h2mab h3mag h3man h3mar h4mäc h4mäh 
h4mäl h4mäu h3me. hme1e hme1in h3men hmen2s hme2ra h2mo h4mon h3mö hm3p4 hm2s 
hm3sa hms1p h2mu 2hn h2na hn1ad h3nam hn1an h2nä hn3d4 hn2e hn3eig hn3ein h2nel 
hne4n1 hne4pf hner3ei h3nerl h3nerz hn3ex h2nic h2nid h2nie hn1im hn1in h2nip 
hn3k4 h2nor hn3s2k hnts2 h1nu h2nuc h2nul hn1unf h3nunge ho2bl ho2ch3 ho2cka 
ho6ckerl hock3t 2hod hoe4 ho2ef ho4fa ho2f3r 2hoi hol1au 4holdy 3hole ho2l1ei 
hol3g4 4holo ho4lor 3hol3s h1o2ly 3holz hol6zene hom2e ho2mec ho2med h2on hono3 
2hoo 2hop ho1ra hor3d h1org ho4sei ho3sl ho2sp ho4st 2hot. ho3th hotli4 2hot3s2 
3hov 2ho2w1 h1o2x ho1y2 1h2ö hö2c hö3ck h4ör hö2s1 h3öst 2h3p2 h1q 2hr hr1ac 
hr3ad h1rai h1rane h3räu hr1c hr3d h2rec h3rech h3red h3ref h4rei. hrei4ba 
h3reic h4r3eig h3rel h3r2en h3rep hr2erg hr2erk h6rerleb hr2erm hr2erz h3re2s1 
hre2t h2r1eta h3rev hrf2 hrg2 h2ri h3ric h4rick hri4e h3riesl h3rin h4rine 
h4rinh h4rist h2rob h3roh h3rol h4rome h4romi h4ron h2ror h3rou hrr4 hr2s1ac 
hr2s3an hr2sau hr3schl hr2s1en hr2ser hr4set hr4s1in hrs3k hr4s1of hr2su hr4sw 
hr2tab hr2tan hr2th hr2tor hrt3ri hr2tro hrt2sa hrt2se h3ruh hr1ums h3rü h4rüb 
h2ry hrz2 4hs h2s1ach h2san h2sau h4schan h2s1ec hse4ler h2s1erl h3s2ex h2s1ing 
h2s1of h2s1par h2sph hs2por h2sprä h2spro hss2 h1sta hst3alt hst2an h2s3tau 
h1stec h3stein h5stell h3s4terb hst2he h1s2ti h1sto h2stor h1s4tr hst3ran 
hst3ri h1stun h2s1u hs2ung 4h1t h2t1a h3t4akt. h3takts h3t2al h4t3alt h4t3a2m 
hta4n ht3ane h3tank ht2as h4t3ass h4tasy ht3a2t h2tär ht1e2c h2t1ef ht1eh 
hte2he h2teif h4teilz h2t1eim h2t1eis h4t3elit h2temp h4tentf h4t3ents ht3erfo 
ht3erfü h2t1erh ht5erken h4terkl h6terneu h4t3erre ht3ersc h6t5erspa ht3erst 
h6tersta ht6erste h2t1erz hte2s h4t1ese h4t1ess hte3sta h2t1eu h2t1ex h2th 
h4thei hthe3u h4tho h2t1in hto2 h2toly h2torg h3töp h4t3rak ht3rand h2t3rat 
ht6raume h4tref ht4ri h4t5rin h2t3rol h2t3ros ht3rö h4t1rös h2t3ru h2t3rü h4ts 
ht2so ht2sp ht3spri ht4stab hts2ti hts4tie ht4s3tur ht4s3tür htt4 htti2 h2t1urs 
h3tü ht3z2 hu2b1a hu2b3ei hu2b1en hu2b3l hu4b3r hu2bu hu1c hu2h1a hu2h1i huko3 
huk3t4 hu2l3a hu2lä hu2l3ei hu4l3eng hu4lent hu2ler hu2let hu2l1in hu2lo hu3m2a 
h1ums hu2n h1una hung4s hu3ni1 h1up. h1ups 2hur hurg2 hu3sa hu2so hus4sa hus2sp 
hu2tab hu3t2h hu2ti hut2t hut4zen hut4z3er hutz1i h2ü h4übs h3übu hühne4 hüs3 
2h1v hvi2 hvil4 2hw h2wall hwe1c h1weib 3hyg 3hyp hy2pe. 2hy2t h1z hz2o hzug4 
i1a 2ia. i4aa i2ab iab4l 2iac i2af iaf4l i4a3g2 i2ah i2aj i2ak i3ak. i3akt 2ial 
i5al. ia2l1a4 ia2lä ial3b ial3d i3alei i3alent i3alerf i3alerh ia4l3erm i3a2let 
i3a4lia ialk2 i3all ial3la ia2lor ial3t4 ia2lu ial3z2 i2am i4amo 2ian ia2nal 
i3and2 ian2e i3ann i2ano i3ant i3anz i2ap ia3p2f ia1q i3ar. ia2ra 2ias i2asc 
ia3sh i2asi i2a3sp ias3s iast4 i3at. i3a4ta i4ate i3at4h 1iatr i3ats i3au ia3un 
2iav 2iä i1äm iär2 i1är. i1ärs i1ät. i1äta i1ät3s4 2i1b i2b1auf ib2bli ib1ei 
i2beig i2beis ibela2 ibe4n iben3a ibi2k i3bla i3ble i2blis ib2o i2b1ö i4brä 
ib3ren ib4ste i2bunk i2bunt ibu2s1 2ic ic1c ice1 ich1a ich1ä i1che ich1ei i1chi 
i2chin ich3l i3chlo ich3m i1cho i2ch3r ich2t3r i1chu ich1w i1ci i3ck2e i1cl i1d 
id2ab4 i3dam id2an i2d1au 1i2dee i2dei idel2ä ide3so ide3sp 1i2dio idni3 i2dol 
1idol. 2i2dr i3d2sc id2s1p idt4 i2dy ie3a4 ie2bä ie2bl ie2bre ieb4sto ieb4str 
ie1c ie2cho ie2ck ie2dr ie1e2 ie2f1ak ie2f1an ie2fau ief3f4 ie2f3l ie2fro 
ie4g5l ie3g4n ie2g3r ie3g4ra iegs3c i1ei i2e2l1a ie3las iel3au iel3d iel1ec 
ieler8geb i1ell ielo4b iel3sz iel3ta 2i1en i3en. i3ena iena2b ie4n3a4g i3e2nä 
i3end i2ene ien1eb ie3ner ien4erf ie4n3erg i3enf i3en3g ienge4f i3enh i3enj 
i3enk i3enm i3enn i3e2no i3enö i3enp i3enr ien2s ien3sc ien3s2e ien3si iens2k 
ien3sp ienst5rä ien3sz ie1nu i3env i3enw i3enz ie1o2 ier3a2 ie2rap i2ere 
ie3r2er ie4rerf ie4r3erz ie3res i3ereu i4eri ierin3 ier3k2 i1ern i3ern. i2er5ni 
ie2rö ier4seh iers2t ier3sta ier3ste ier3te iesen3s4 ies2sp ies2s3t ie1sta 
ie3su ie2t1a ie4t3erh ie4t3ert ie2t3ho ie4t1o ie4t1ö4 ie2tri iet2se i1ett ieu2e 
ie1un i1ex 2if if1ar i2f3arm if4at if1au i2fec ife2i if2en ifens2 if1erg if1erh 
if2fl if3l i1f4la if4lä i1flü if3r if4ra i1frau i1fre if4rei if4rü if2s if3se 
if3sp if2ta ift3erk if2top if4t3ri ift3s2p ift3sz 2i1g iga3i i2g1ang ig1art 
iga1s4 i4gefar ige4na ig1erz i2g1im i2gl ig1lä ig4na i4gnä i3g4neu ig4no i3go 
ig4ra ig3rei ig4sal ig3sä ig4se ig3so ig3spr ig3stei ig4sto ig4stö ig3str 
ig4stre ig3stü igung4 2i1h i2h1am i2har i3he ihe1e ihe4n ih3m ih3n ih3r ihs2 
i2h1um ih1w ii2 ii3a4 i1ie i3i4g i1im i1in i1i4s i2is. ii3t i1j 2i1k i2k1a4k 
ik1amt i2k1ano ik1anz i4kanze ik1art ik3att i2k1au i2kär 4ike i2k1ei ike2l1 
i2k1e2r2e ik1erf iker6fah i2ker2l i2k1eta i3ki. ik1in i2kind i2k3l i3kla i3k4lä 
i2kn ik3no ik2o3p4 iko3s i2köl i2k3ra ik3rä ik3re ik1s2 ik3so ik3sz ikt2e 
ikt3erk ikt3r ik2tre i2kun i3kus i1la i2l3ab il1a2d i2l1ak i2l3a2m il1ans 
il1asp il1au il4aufb il3aus i2laut i1lä1 6ilb il2c il2da il4d3en4t ild2er ild1o 
il2dor il2dr il1e2c ile2h il1ehe il1ein il1el i4lents i2l1erf i2l1erg i2l1err 
ilf2 il2f3l il2f3re ilf4s3 ilie4n ilig1a2 ili4gab i2l1ind i2l1ip i3lip. i3lips 
2ill. il3l2a il3l2er il3l2i 2ills il2mak il4mang il2m3at il2mau il2min 2ilo 
i2l1or il3t2h i1lu2 i2lum ilung4 i3lus ilv4 il2z1ar ilz3erk 2im. i2manw i2m1arm 
im4at ima2tr imat5sc ima4tur i2meg i2mej i2mek i2mele i2melf i2m1erf i2m1erz 
i4mesh i2meti i2mew i2m1inf i2m1ins im2mei im4m3ent 1immo 2imo im1org 1impo 
imp4s im3pse 1impu im2st im3sta 2imt imt3s2 2imu in3a2c i4nack i2n1ad in2af 
in3am i3nap in2ara in2ars ina4s i2n3au in1äs in2dal in2dan 1index in3do 2indr 
ind4ri in3drü 1indus 2ine i2n1e2be in1ehe in3ei i2n1eng in3erbe i4nerbi in2erh 
iner4lö i4ner4tr i4nesk in1eu ine3un ine2x in3f 1info. 1infos 2inga ing1af 
in2g1a4g in2gl ing4sam 1inhab 2inhar 2inhau 4inhe in2i3d i3nie 2inig ini3kr 
in2ir 2inis ini3se i3nitz 3inkarn inma4le 2inn. in4n3erm 2innl in2nor inn4sta 
1innta 2ino in1od in3ols in1or ino1s2 ino3t i1nö in1ö2d 2inp 2inr ins2am insch2 
in2seb 2insen ins3ert in3skan in3skr 1insta in4s3tät in3stel in3su 1insuf 
in4s3um in3s2z 1integ int2h in3t4r in5tri in1u i3n2um in3unz invil4 i1ny in3zw 
i1ñ 2i1o io1c io2d i2oda io3e4 iof4l i2o3h io2i3d io3k4 i3ol. i3om. i3oms ion2 
i3on. ional3a io2nau ion3d i3ons3 ion4spi ion4st i2ony i2o1p io4pf i3ops i3opt 
i2or i3or. i3orc iore4n i3orp i3ors i3ort io3s2 i2ost i3ot. i3ots i2ou i2ov 
io2x i3oz. i1ö2k i3ön i1ös. 2ip. i1pa i1pe ipen3 i3per ip3fa iph2 2i1pi ipi3el 
ipi3en ipi2s ip4l ip2pl ip3pu i1pr 2ips 2ipu 2i1q i1r2a i3rad 1i2rak irat2 i1rä 
ir2bl ir1c ir2e i3ree 2irek 2i3ré ir2gl irg4s ir2he ir2i 2irig 2irk ir2k3l 
irli4n ir2mak ir2mau ir4mä ir2m1ei ir2mum ir4m3unt ir2nar ir2no i1ro 1iron 
iro2s i1rö irpla4 irr2h ir4sch3w ir3se ir3sh ir2st irt2st iru2s1 i3sac i4s1amt 
is2ap is3are i2sau i2s1än 2isb i2sca isch3ar i3s2che i4schef i4sch3e4h i4sch3ei 
i4schin i5sching i2sch1l isch3le i2schm isch3ob isch3re isch3ru i4schwa 
i6schwir i4schwo isch3wu is1chy i2s3cr 2ise ise3e ise3ha ise3hi ise3inf i4seint 
ise2n1 is2end isen3s i2serh i2s1erm iser2u i2s1ess i4s3etat is2has isi2a i2s1id 
i2s1of iso6nend is1op 3i2sot is1pa i2spar is1pe is1pic is2pit i2spro is3sa 
is4s1ac is4sau is4s3che is2st is3sta is3sto iss3tr is3stu is2sum is3t is4tab 
is4tam ist2an i1s4tat is4tel iste4n istes3 i1s4teu i1s4til is4toc is4tö is5tör 
ist4ra ist3re is4tü isum3p i2sü i1ß iß1ers it1ab. ital1a it1alt it1am it1an 
it2an. it3a4re it1art i3tat it1au i3tauc i4t1ax 4itä it2är i2t1äs ität2 i2t1ei 
i4teig it2eil i4tein 2itel ite2la ite4n iten3s2 i4tepo i2tex i5thr i2t1id 1itii 
iti4kan i2t1in1 it2inn itmen2 i5toc i2t1of i3tö it3raf i2t3ran it3ras it3rau 
it3räu it3re it3ric it3rom it4ron i3tru it3run it2sa its1a4g it2s1e4 its3er1 
it2so it2s1pe it4staf it2sto it2teb it4tri itt2sp it1uh i2t1um i2tuns it1urg 
itut4 i3tü 2itz it2zä it4z3erg it2z1w 2i3u2 ium1 i1ü 2i1v i2v1ak iv1ang i2veb 
i2v1ei iv1elt ive4n i2v1ene i2v1ent i2v1ur 2i1w iwur2 2i1x i2xa ix2em i3xi 2i1z 
iz1ap iz1au izei3c ize2n i2z1ene iz4er i2z1ir izo2b i2zö i2z1w í1l ja1c 
jah4r3ei jahr4s ja3l2a ja3ne jani1 ja1st 2jat je2a jean2s je1c je2g jek4ter 
jekto2 jektor4 jek2tr je3na je2p je4s3t je2t1a je2t3h je2t3r jet3s2 jet3t 
je2t1u2 je3w ji2a jit3 ji2v joa3 jo2b1 job3r jo2i joni1 jo1ra jord2 jo2sc jou4l 
j2u ju2bl jugen2 jugend3 ju2k jung3s4 ju3ni jur2o jus3 jut2e1 2j1v 1ka 3ka. 
k3a2a ka3ar kab2bl ka2ben 2kabh 2kabla 2kablä 2k1a2bo ka3b4r 2kabs 2k1abt ka1c 
k2ad 2k3ada 2k3a2dr ka1f4l ka1fr kaf3t2 k2ag ka1in ka3ka kaken4 2kala. ka2lan 
ka3lei ka3len. ka4lens kal3eri kal2ka kal2kr k1all kalo5 kal4tr k3ama kamp8ferf 
kan2al ka4n1a4s ka2nau kand4 2kanda kan2e 2k1ang kan3k4 2kanl 2k1anna k1ans 
k2ans. 6kantenn ka3nu 2kanw k2anz. ka2o 2k1apf 3kara 2karb k2ard k2arg ka3r2i 
kari3es k2ark 2k1arm k2arp3 kar2pf k2ars kar3t k2arta 2k1arti karu2 k2arw 3kas 
ka3se kasi1 kas3s ka2s3t ka3tan ka3t4h ka4t3r 2katt kau2f1o 4kaufr kauf4sp 
k1aus kau3t2 2kauto 1kä k1äh k1ä2mi k1än kär2 kä2s1c käse3 2k3b4 kbo4n kbu2s 
kby4 2k3c 2k3d2 kdamp2 2k1e1c k1eff kefi4 kege2 ke2gl ke2he. kehr2s kehr4s3o 
2k1eic 2k1eig k1ein ke1in2d 2keinh kei1s 2k1eise keit2 ke2la kel1ac ke3lag 
kel1au ke2lä kel3b4 2ke2lek ke2len 2ke3let kell4e kel3s2k k4elt 2k1emp k2en. 
ken3au 4ken4gag 2kenlä ke2no kens2k ken5stei ken3sz k2ente k3enten ken3th 
k2entr 2k1ents k2entu 2kentw 2keo2 ke2pl k2er. ke1rad k2erc 4kerfah k4erfam 
k3ergeb ker6gebn k3er4hö ke6rin6nu kerin6st kerin4t ker4ken k2erko k2erl 
k3er4lau k3er4leb k6erlebe ker4neu k1e2ro k2ers. kerz2 ker4zeu 2k1er2zi k6es. 
ke2sel ke4t1a ke2t3h ket3s ke1up keu6schl 2k1e2x 2k3f4 2k1g2 2k1h4 kho3m ki3a4 
ki1c 2k1i2de ki3dr ki2el kie2l3o ki1f4l ki1f4r ki3k4 2kil2a ki3li ki3lo k2imi 
k2in. k2ing 2kinh k2ini k2inn ki3n4o3 kin3s 2k1inse 2k1int ki3or kio4s 3kir 
kis2p kist2 kis4to 2kiz ki3zi 2k3j 2k1k4 kl2 4kl. 4kla. k4lar 4k1last k2le 
4kle. kle3ari 4kleh k4leid 4k3leit k3lem. 2k3ler kle2ra 2k3leu kle3us 2klic 
2klig k2lin k3lip k2lir k2lisc 2klist klit2s 4kliz 2k3loc klo2i3 k4lop klost4 
klö2s k2löt k1lu kluf2 klung4 2k1lüc 2kly 2k1m k2n2 3knab k3ne k4nei 2k5ner 
kno4bl 2k5nor k3nu 3knü 1ko ko2al 2kobj 2k1o2fe koff4 koh3lu ko1i2 kol4a ko3le 
kol2k5 3kom ko4mu k2on ko3n2e kon3s4 ko3nu 2kop. ko1pe kop4fen 2kops 2kopz 
ko1r2a 2k1orc kor6derg ko3ri k2os ko2sp ko2st ko3ta kot3s2 kot4tak 2k1ou 3kow 
ko2we k1o2x 1kö kö2f k1öl 2k1p2 k1q k2r4 2k3rad k3rats 2kraum k4raz 2k3rät 
2k3räum 2kre. 2k3rec 2k3rede 2k3ref 2kreg k3reic kre1i2e4 kreier4 k3reih 2k3rh 
2krib 2k3ric k3ries 2krip 3kris 3k4ron 2kruf krü1b 2ks k4s1amt k2san ks3ar 
k2sau ks2än ksch4 ks1e2b k2s1em k2sent ks1erl k2s1ers k2s1erw ks3ha k2s1id 
k2s1in k2s1o2 k3sof ks1pa k3spe ks2por ks2pu ks3s2 kst4 k1sta k4s3tanz k3stat4 
k1ste k1s2ti k1sto k2stor k1str k2strä k1stu k2stum k2s1u ks2zen 4k1t k2t1ad 
kt1akt k3tal kt1am kt1an k2t3a2r kta4re k2t1au ktä3s kte3e kt1ei k2temp k2tent 
k4t3erfo k2t1erh kte3ru k2tex k2th kt3ho k2t1id kt1im k2t1ing kt1ins kti4ter 
k2t1of k3top kt1ope k4torga kt3orie kt4ran kt3ras k4tref kt4ro ktro1s kt3run 
kt3s4 ktt2 k2tuns k3tü kt3z ku1c kuh1 2k1uhr kul2a ku3l2e ku3l2i 4kulp 2k3uml 
kum2s1 k2u3n2a kung4 kun4s4 kunst3 2kunt 2k1up. kur2bl ku2rei kuri2e kuri4er 
ku2ro kur2sp kur2st ku4schl ku2sp kus3t ku2su 1kü 2küb kü1c kür4s 2k1v 2k1w 
2k3z2 kze3l 3la. la3ba 2labb 4l3aben 2labf 2labg 2labh 4l1a2bl lab2o l2abr 
lab4ra lab4ri 2l3abs l1abt 3labu 2labw la1ce la2ce. 1lad lad2i l1adl 2ladm 
2l1a2dr 3ladu l1adv 2laf la2fa laf3s laf3t la2ga la2gio la2gn lago2 la2g1ob 
2la1ho 1lai la2k1i l2akk la1k4l 2l1al 4lall 4lalp l2ami la3min 1lammf l2amp 
2l1amt lamt4s la4mun l1anal la2nau 2lanb 3l2and lan2d3a2 lan6d5erw lan6d5erz 
lan2d3r 2lanf lan2gl lang3s4 2lanhä l2anhe 2lanl 4lanli 2l3ann l1anp 2lans 
4lansä 2lantr lan2zw 3lao l1a2po2 lap4pl la2r1an la2r1ei la4rene 3l4ar3g 
lar3ini lar3s 2l1ar3t l3arti la2ru la2sau 4lasd la3se 2lash 2lasi la2so 2lasp 
3lasser la2st last1o lat2a la3te la4tel 2l3ath la2t3ra lat2s 2lat2t1a lat4tan 
lat4t3in lat2t3r laub4se l2auf. lau2fo l2aufz 1laug 2lausl 2lausr 2l1auss 
2lauto 1law lawa4 lay1 lä1c 1läd 2läf 2l1ähn 1länd lär2m1a lä2s1c 4lät 2läub 
2läuc 2läue 1läuf 1là 2l1b l3bac l2b1ede l4beta l2b1id l2b1ins lb2lat l3blä 
lb3le l2bli l3blo l4bre. lb3rit lb2s lb3sa lb3se lb4sk lb3sp lbs6t lbst3e 
lb4sto lb2u l2b3uf lbzei2 2l1c l3che l3chi lch3l lch3r lch3ü lch1w l3cl 4l1d 
ld3a2b1 l3d2ac ld3a2ck l2d1a2d lda4g l2d1ak ld1al l3dam ld1amm l2d3a2n l2d1a2r 
ld3ari l3das l3dat ld1au ld1är l2dei l2dele l3der. ld1erp l2d1e2se l2dex l2d1id 
l2d1im ldo2r ld2os ld2ö2 ld3r l2dran l2dre l3d4ru ld4rü ld3sa ld3st ldt4 ld3th 
l2d1um 1le 3le. le2ad leben4s3 le2bl 2lec le2chi lecht4e 3led 4ledd le3de le2e 
le3ei lef2a le2g1as le2gau le2gä le2gl leg4r 3leh leh3r2e 4lehs 4leht 3lei. 
lei2br l2eic l2eid 4l1eig l2ein. l2eind lein4du l2eine lei6nerb 2leink l2eint 
leis6s5er l4eist lei4ßer l2eit lei2ta lei8t7er8sc leit3s2 lekt2a 2lektr 3l2ela 
2le2lek lel3s 3lemes le2m1o2 4lemp lem3s l2en. le4nad le2nä 4lendet 2lendu 
le4n3end 4lenerg l2enf le3ni l2enk 2l1enni l2e2no len4sem len3sz l1ents 2l3entw 
lent4wä 5lentwet 4lentz len2zi le1os 2lep 3lepa 3lepf lepositi8 3lepr l2er. 
l2e1ra le2ra4g le2rau lerb4 4l3ereig le4r3eim le4rers l1erfo l2erfr l2erfü 
3lergeh l3ergen 3l4ergew 2l1ergi lerin4s lerk2 l2erka l2erko l2erle 2l1er2ö 
3l2erra l4ers. lers2k lers2t ler3t 6lerwerb l1erz l2erza les2am les2e 2l1esel 
le3ser le3sh lesi1 le3sk les2t leste3 le1sto 4lesw 2lesy le2tat 2le3th 2leto 
let4tu le2u 4leud 2leuro 3leut 3lev 2lexe le2xis 2lexz 2l1f l3fah lfang3 l2f1ec 
lfe1e l4feis l3f4lä lf3lo l3f4lu lf3ram lf2tr lf4u lfur1 l3fü 2l1g lga3t lgd4 
lgen2a lge3ra lgeräu3 l2geti l3go lg3re l3gro 2l1h2 3lhi. 1li 3lia li3ac li3ak 
li3ar lia1s libi3 li1c 3lichem 3licher li3chi 4lick li2cka li3d2a li2deo 2l1ido 
li4ds lid3sc l2ie 3lie. liebe4s li3ene lien3s lie2s3c lie2st 3lig lig4n li2gre 
li3ke li2kr lik2sp lik4ter li3l lil2a 2lim li3m2a 3limo li3n2a lin3al 2l1indu 
li2nef li2neh li2nep li2nes 2l1inf lings5 2l1inh 2l1in1it 2l1inj lin2k1a link2s 
li2nol l2ins. l2insa l2insc 2linsp 2linst 2l1int l1inv 2linz li2o li4om li3os. 
li2p3a 3lis. li3s2a li4schu 4lish 2l1isl 2l1i4so li2sp liss2 lit2a li2tal li3te 
lit2h lit1s2 lit3sz li3tu 3liu 2lixi li2za lizei3 4l1j 2l1k lk1alp l3k2an 
l3kar. lken3t lk2l lk3lo l3k4lu lk4ne lkor2b1 lk4ra l2k3ro l2k3ru lk2s1 lk3sä 
lks3t lk4stä l3k2ü 4l1l ll1abb ll1a2be l2labt ll1aff ll1akt l3l2al l2l1a2m 
ll3ama lla2n ll2anw ll1anz l3lap ll1arm ll1au ll3aug l2laus l2l1äm llb4 llch4 
ll3d4 ll1ech lle3en l2l1ef ll1eim ll2em l3len. lle4n3a ll3endu llen3g l4lents 
l3ler. lle2ra l4lerfo l6lergen l4lergo ll3ernt ll3ertr l2lerz ll2es l2lex llg4 
ll1imb ll1imp l2l1ind ll1ins llk4 ll3l2 ll5m lln2 ll1ob l2lobe l2l1of ll1opf 
l2l1o2r l3lor. l3lore l2l1ou l3low l2löf ll1ö4se ll3sh ll3s2k ll2spr ll5t4 
llti2m llt5s2 llu2f ll1ur llus5t6 ll3z2 2l1m l2m3a2b l2marc lm1aus lm1c lme2e 
lm3eins l2m1e2p l2m1erz lm1ind lm1ins l2möl lm3p lmpf4 lms2t lm3ste lm3s2z lm3t 
4ln lna4r ln3are lnd2 l3n4e l3ni l1nu l1nü 1lo 3l2ob. lo2ber 2lobj 2l1o2bl 
l2obr lob4ri l1o2fe lo1fl lof4r lo2gau lo3h2e 2l1ohr loi4r 3lok lo2k3r lol2a 
l1o2ly lo2min lo2n1o lo2o 2lopf 2lopt lo1ra lo4rä 2lorc l1ord lo3ren 2l1or3g2 
lo3ro 3lorq 3los. lo4sa 3lose lo4ske lo2spe loss2e lo4ste los3t4r lo2ta lo3tha 
loti4o 2l1ov lo2ve 2lox 1lö lö2b3 2löd lö2f 2l3öfe 4lög l1öhr 2l1ö4l3 4löß 2l1p 
l3pa lpe2n3 lp2f l2p1ho lp3t4 l3pu 2l1q 2l3r2 lrat4s lre1s lrut4 lrü1b 4l1s 
l3sac l2s1a2d l3s2al l4s1amb l2sann l3sare l2sau l4schin l4schmü l2s1e2b l2s1ec 
l2s1em ls1ere ls1erg l2serh ls1erl l2s1ers l2s1erw l3sex l4sha lsho2 l2s1imp 
ls2log ls3ohne l4s3ort. l3s2pi ls2po l2spro l3s2pu ls3s2 lst2a lstab6 ls4taf 
l4s3täti l2ste l3stec l3stei l3stel l4stem ls6terne ls6terns ls2tie l2stit 
ls4tr ls2tu ls1um l2sun lsu3s ls2zen 4l1t l2tab ltag4 lt1ak lt1a2m l4t3ame 
lt3and lt1ang l3tarb lt1art l2t3ato l2t1au lt1eh l2t1eis l4te4lem lt3eli lt2en 
l5ten. lter3a lt2erg lt4erö l4t1e4sk lte2th l2t1eu l2th l4thei lt3ho l3thu 
ltimo4 l2tob l2t1of lt1op l2t1o2ri lto2w lt1öl l3tör lt1ös l4t3öt ltra3l l3trä 
lt3räu lt3re lt4rie lt3roc lt3ros l2t3rö l6ts lt3sc lt2so lt4stab lt4stoc ltt2 
lt1uh l2t1um ltu4ran ltu2ri l3tü lu1an 4lu4b3 luba2 lubs2 lu2dr lu2es 1luf 
2l1ufe 2luff luf2t1a luf2t1e luf2t5r lu2g1a lu2g1e2b lu4g3l lu2go lu2g3r lug3sa 
lug3sp lu2gu 2l1uh lu1id. lu1is. lume2 2lumf 2luml l2ump l1ums l1umw 1lu2n 
2l1una 2l1unf lung4sc 2l1uni 2lunt 2lunw 4luo 2lur l1urn l1urt 2luse lu2sp 
lus4s3a lus2s1c luss3er lus6serf lus6serk lus6sers lus2s1o lus2s3p lus2s3t 
lus4stä lu4st lus4t1a lust3re lu2s1u lu2t1a lu2tä lu4teg lu4t3erg lut1o2f 
lu2top lu4t3r 3lux 2lüb 5lüd lüh1l 2l1v 2l3w 2lx 1ly ly1ar ly3c 2lymp 3lyn 
ly3no ly1o ly3u 2l1z l2z3ac l3z2an lz2erk lz1ind lzo2f l2zö lz3t2 l2z1u4fe lz1w 
lz2wec 1ma m1ab m2abe 2mabk m2ab4r 2mabs 2mabt mach4tr ma2ci ma3da ma2d4r 
ma4d2s mae2 ma1f ma2ge. ma2geb ma2gef ma2geg ma2gek ma2gep ma4ges. ma2get 
ma2gev ma2gew 2m1agg magi5er. magi5ers ma3g4n 2m1ago mai4se 2m1akt mal1ak 
ma4lakt ma2lan ma4l3at ma2lau mal3d ma3ler mali1e mal3lo 2mallt malu4 ma2l3ut 
mam3m 2m1anal ma2nau 2manb man4ce. man3d2 man3ers ma2net m2anf 2m1angr m2anh 
2manl m4ann 2mansa 2mansä 2mansc 2mantw 2manz ma2or m2app 2marb mar3g2 4ma3r2o 
maro3d 4marr mar6schm mar6schr ma3r2u m1arz 3mas ma3s2pa 4m1aspe massen3 
mas4tel ma1s4tr 3maß ma2ta2b ma2tan mat4c ma2tel ma4t3erd ma5tri mat3se mat3sp 
2m1au2f ma3un 2mausg m4ay ma1yo 3mä m1ähn mä1i2 4m1änd m1ärg mä3t4r mäu2s1c 
2m1b2 mbe2e mb4l m3b4r mby4 2mc m3ch 2m1d md1a m2d1ä m2dei mds2e m2d1um 1me 
meb4 m2e1c medi3 medie4 medien3 2medy me1ef mee2n1 mega1 3meh 2m1eif 2m1eig 
m2eil mein4da me1i4so 3meist me3lam 3meld me2lek me2ler melet4 2melf. mell2 
mel2se mel5t4 6mel6tern 2m1e2mi m2en. mena2b me3nal men3ar men3au men3gl me3nor 
m2ens men4sk men2so men3ta men6tanz 2mentn 4m3entwi me1o 2meou 2meö 3mer. me1ra 
me2r3ap me4rens mer2er 4m3ergän 3merin merin4d merin4t me2ro 3mers merz4en 3mes 
mes1a me2sal me4sä 4meser 2me3sh 4m1essa mes6serg mes2s1o mes2s1p mes2st meste2 
me1sto 4mesu me3t2a me3th meu1 2m1ex 1mé 2m1f4 mfi4l 4m1g2 2m1h4 1mi mi2ad 
mi3ak mibi1 mi1c mi3da mie3dr mi2e1i mie3l mien3s mi2er mierer4 mie2ro mi4et 
mie4ti 3mig mi2kar mi2ki mi2ku 3mil mi3l2a milch1 mil4che mild4s 4milz 2m1imp 
minde4s min2en min2eu min2ga ming3s4 mi3ni 3min2o mi1nu 3mir. mi3ra 3miri 3mirs 
3mirw mi2sa mi4scha mi4schn mi4schw mise1 mis2s1c mi2s5te 3mit mi2ta mi2th 
mi2t1r mit3s2 mit5sa mi5tsu mi2t1u 4mitz 2m1j 4m1k4 m3ka mk5re. 4m1l2 ml3c ml3l 
ml3s 2m1m m2mab m2m1ak m2m1al mm1ang m2m1ans mm1anz m2m1au mmd2 mm1ei mme4lin 
mme4na m4mentw mme2ra2 mme4rec mme2sa mm1inb mm1inf mm1inh mm1ins mm1int mmi3sc 
mmi1s4t mmm2 mm3p mm2s mm3si mm3sp mm3sta mm3str m2mum mm2un mmül2 mmüll1 2m3n2 
m4nesi 1mo moa3 2mobj 3m2od mode3s mo2dr 4mog. mo2gal 3moh mo2i3 mo2k1l 2mol. 
3mom mom2e 3m2on mo3ne mo4n1er mon2s3 mon3su 3mo2o 2m1ope 2mopt mo1ra mo2rar 
2m1orc mor2d3a mor2dr mo2rer morgen5s6 mork4 3mos mos4ta moster4 3mot m1o2x 
mo1y 1mö mö2c 4mök m1öl 2m1p m2pf mp4f3erg mpf3erp mpf3err mp4f3erz mp2fl 
mpf3li mpf1or m3pon mp3ta m3pu 2m1q 2m3r2 2m1s m2san ms3and m4sap ms1as m2sau 
m3sä m3sc msch2 m4sco m3se m4s1ef ms1erw m4sex ms1ini mso2r ms1ori m2spä m2sped 
ms2po m2spot m2spro ms2pu ms3s2 m4stag m3stel m3s2ti m3sto ms4tr ms5trä ms5tren 
m3s2tu ms4tü ms1um m2sü m3sy 4m1t mt1ab mt1ak m3tam mt1ar mt3are mt1elt m2t1erf 
m4t1erg m2t1erl m2t1ers m2t1ert m4t1eta m2t1eu m2th mt3ho m2t1im m2t1ins mti2s 
mtmen2 m3tö mt1ös m4ts1 mt2sa mt2se mt3s2ka mt2spr mtt2 mt1um mt1urt m3tü mt3z 
1mu mu1a mu3cke 2m3uh mu3la 2muls 3mun mun2d1a 4m3unf 4m3ungeb mu3ni m4unk 
munt2 4munz mu3ra mu4r1u2f m4us mu4s1a 3musi mu2s1o mu2sp mus3t mu2su mut1au 
muts3 mut2st 1mü 2müb mül4len 3mün 3müt mütter3 2m1v mvoll1 2m1w2 mwa2 mwa4r 
mwel4 1my my4s 2m1z 1na 3na. 2n1ab na2bä 4nabg 4nabh na2bl n2abo na2br 4n3abs 
4nabt 3n2ac na2ch1 na3chen nach3s nacht6ra 4nadd n2ade 4na2dr n1af na1f4r 3n2ag 
na2gem 3n2ah na2h1a n3ahn 3nai nai2e n3aig n3air 2n1ak na2ka 3nako n2al. 
na2l1a2 na2lä 3n2ald n4ale na4lent na2let nal3la nalmo2 na2lop nal2ph n2als. 
nal3t4 na2lu 2naly n4am. 3name n4amen 4n3a2mer na3m4n 3namo 2n1amt namt4s n1an. 
4n1a2na 4nanb n1and2 4n1ang 2nanh 2nani 4nank 2nanl 3nann na3no n1anp 2nanr 
2n1ans 2nantr 2nanw nap2si n1ar 5nar. na2r1a 2narc n2ard 4narg 3nari n2ark 
n2arle 2narm n2arp 4n3art na3r2u 3nas n2as. na4schw 4nasp 4n1a2sy nasyl2 3nat 
n4ata na3t4h 4natm nats1 nat4sa nat4sc 4natt n1au 4nauf nauf4fr n3aug 5naui 
3n2aul 4nausb 4nausg n2auso 4nauss n4auste 4nausw navi5er. navi5ers 1nä 3n2äc 
3näe n1ähn 2n1ä2m 2n1än när4s5 3näs nä2sc n2äss 2näu 3nä1um 2n3b4 nbe2in nbe3n 
nbe3r2e nbes4 nbu2s nby4 2n1c n3ce2n3 nch3m n2ck 2n1d nd2ag n2d1ak n2danl 
nd1ann n2d1anz ndat2 nd1au nd1c nde4al. n2dei nde4län n4d3ents nde4rob nder5ste 
nde2se ndi2a3 n2dob ndo2be ndo1c nd1op nd1or n2dö n2d3rat n2d3re n2drob nd3rol 
nd3ros n2drö n2drui n4d3run nd2sor nd2spr nd4stab nds3tau nd3th ndt4r n2dü4 
ndy3 1ne 3ne. ne2ap ne3as ne3at ne2bl 2n1ebn 2nec 3neca ne1ck 3ned ne2de 2nee3 
ne2e2i4 ne3ein n1ef neg4 2ne2he. 3nehm 4n1ehr 2n1ei n2eid 4neif 3neigt 4n3eing 
4n3eink ne2ke nek3t4 ne2l 3nela nel3b 2n1ele 4nelek 4nelem ne3len ne3li nel4la 
3ne3l2o 3ne3lu n2em. 2n1emb n1e2mi 2n3emp 2n1ems 3nen n4en. nen3a2 n2enb n2enc 
4n1endb 4n1endd 4n1endf n1endg 4n1endh 4n1endk 4n1endp 4n1endt 4n1endw ne2n1e2b 
nen3ei nenen1 ne4nene 4nengb nen4ge. nen4gen 4nengs 4nengt n2enh ne2ni n2enj 
nen3k ne2no n2ens nens4e nen3sk 5n2en3t2a n1entb 4n1entl 4nentn 5nentr n1ents 
4n3entw 4nentz ne2n3u n2env n2enw ne2ob ne1os 2nepf 2n1epo ne2pos n2er. ne1ra 
ne2ra2b ne3r4al ne2r3am ne2ran ne2rap ne2rau 4nerbe. 4nerben n1erbi nere2 
ne2reb n1erf 4n5erfo nerfor4 2nerfü 3nergr n1erh 2n3erhö 3neri n1erk n2erli 
2n1erlö n1ermä ner4mit n2ern. 4n1ernt ne2ro ne1rös n2erp 3n2ers. 2n3ersa 
ner8schle n2ert. n1ertr ne2rup n2erv 2n1erz 3n2es n4es. ne3san nes4c nesi1e 
ne3ska nes1o ne2s1p 4n3essi ne1sta nes3ti ne2tad ne2t1ak ne2t1an ne2tap n1etat 
ne2tau ne2th net3ha nett4sc n1e2tu net2zi ne2u neu1c neu3g 2n1eup n2ew 2n1ex 
3nez 1né 2n1f nf1ak nfalt4 nf2ä nff4 n3fi nfi4le. nf4l nf5lin nf2o nfo1s nf4r 
nf3s nft2o nft4s3 n2f1u 4n1g ng2abs n2g1ac ng1ad n2g1ak n2g3a2m n2g1and ng2anf 
ng1anz n2g1äl ng3d4 n3gef n2g1ein ng2en ngen2a n3ger nge4ram n4g3erse nge4zän 
ng3g4 ng3hu n2g1i2d n3gläs n2glic n2glo n3g2loc n2glö ng3m n2gn ng3ne ng1or 
ng3rat ng3roc ngs3c ng4s3e4h ngs3pa ngs5tri ng3ts n2gum 2n1h4 n3han n3har n3hau 
n3hä n3he nhe2r n3hu 1ni 3nia nib4l nich1s nich8ters n1id ni2de ni3de. ni3dr 
n4ie nie3b ni1el nie3l2a nie4n3 ni3ene ni1ero nifes3 nig2a 2n3i2gel nig3r 
ni2gre nig4sp 3nik ni2kal ni2kar ni3ker ni4k3ing ni3kl ni2kr 3n2il nim2o 4n1imp 
nin1 3n2in. n2in4a 4n3ind 2ninf 3n2ing4 4n1inh ni2nor 2n1ins n2ins. 4ninse 
4n1int 2n1inv ni2ob ni3ok ni3ol n2ip ni3ra 3n2is ni4schw ni2s1e ni2s1p ni3spi 
nis3s4 ni2s1u 2nit ni2ti ni3t4r nit4s ni3tsc nitts1 nitt4sa ni3tu ni3v 3nix n1j 
2n1k n2k3ad n2k1ak n3k2al n4k3alg nk2am n2kans n2kaus n2käh n2k1är nke2c 
n4k3erfa nk4erg nk1inh n2k1ins nk3len nk3les n2klie nk2lo nk2lu nk3lun nk4na 
n2kne n2k1ort nk2öf n2köl n2k3ro nk2s1al nks2ei nk3s2z nk2tak nk2tan nkt1it 
nk4top nk2tru 2n3l2 2n1m4 nmen2s 4n1n nna2be n2nada n4n1all n2n1an n2nau nnen3g 
n4nents nn2erh nn2erk nne2rö n4n3er4wa nner2z nne2s nnes1e nne4st nn2ex nn3f 
nng4 n3ni n2nof nn1o2r nn3sc nn3se nn3s2p nn2th n2n1uf n2n1unf nn1ur 1no 3no. 
3nobl no2bla n2o3ble 2n1ob2s no1c 2no2d no3dr n1of 2n3o2fe n3ole no2leu n2on. 
3n2opa 3nor. nor2a no2rad no1rak no3ral 2norc nor2d5r 3norh 3norm 3nors n1ort 
3n2os. no3sh no2sp n2oste nost1r 2nostv no3tab no2tä no4t3ei no2tel no3t3h 
no4tha no2t3in no2t1op no2tr 3nov 3now 2n1o2x 3noz 2nöd 2nö2f 4n1ö4l 2n3p4 
npa2g npro1 npsy3 2n1q 2n3r2 nräu3s nre3sz nrö2s1 6n1s n2s1a2d n2s1all n2sang 
n2sant n2saus n3sav n2s1än n2s1äus ns2ca n6schef n4schro nsch7werd ns1eb ns1e2d 
nseh5ere nsen4sp ns1ent n2s1ep ns1erf ns1erg n2serh n2s1erk n2s1erö ns1ers 
n2s1erw n2s1erz nse2t n4s1eta n3sex nsfi4l nsho2f n3sil n2simp n2s1ini nsi4te 
nsi2tr ns2kal n2s1op n4s3ort. nsp4 n2spat n2sph n3s2pi ns4pie n2spo ns3pon 
n2sprä n4s3prie n4spro nsrü2 ns3s2 nst1ak n3star n3stat n4stat. n4s3tate 
nst3eif n3stemm ns4tent ns6terbe n5s6terne n5s6terns nst4erö ns2ti nst5opfe 
ns4tor n4strac n4strie ns2tu nst2ü nstü1b n2sty ns2um n2s1un ns2ung ns4unr 
ns4uns n3sy n4s3zi 2n1t nt3abs n3t2a3c n3t2al nta3m nt1ang n4tanza nt2arb 
nt1ark nt2arm nt4at nt1äm n2t1äu nte3au nte2b nt1ebe nte1e nte3g6 nt1eh n2teig 
nt2en nt4ene nten6te. n3ter nt4ern nt4ers nt4ert n4t1ess nteu3 nte3v nt2her 
n2t3ho n3thr n3t4hu nti3c nti3k4l n2tinf n2t1inh ntini1 nt2ins n3ti1t ntmen2 
ntmo2 n3to nto3me nton2s1 n3tö nt3rec nt3reif n5trep nt4rig n5trop n2t3rü n4ts 
nt3sa nt4sau nts2o nts2p nt4s3par nts2t nt2sto n3tu 3n4tu. ntum4 ntu2ra ntu4re. 
ntu4res n3tü nt3z2 1nu. 1nu1a nu3ar nubi1 1nu1c 1nud 3nue nu2es nuf2 nu2fe 1nug 
2n1uh 1nui nu3k4 n2um. 2n3umb 2numf 2numg 3numm 2numr 2n1ums 2n3umz nu2n 2nuna 
1n2ung4 3nung. n3ungl 2n1uni 2nunt 1nuo 2nup 2nur 3nu2s nu3sc nu3se nu3sl 1nut 
nu2ta nu4t3r 1nuu 1nux 1nuz 3nü. 2nü4b nür1c 3nüs 1nüt 2n1v2 n3ver 4n1w 1ny. 
1nyh 2nymu n1yo 1nyr 1nys 1nyw 2n1z n2zad n2z1a4g n2zan n2z1au n2z1än n2zär 
nzdi1s nz1ec n4zense n4zentw n4zentz nz3erwe nzi2ga nzig4s nz1ini n2zor nz2öl 
nz3s n2zurk n2z1wa n2z1wä n2zwö n2z1wu ño1 2o3a2 o4abi o4ac oa3che oa3chi o4ad 
oa3de oa4g o4ah o4a3i oa3ke oa4k1l o4a3la o4a3mi oanne4 o2ar o2as 3oa3se o4at 
o5au o1b ob2al 2oban o3bar 2o3b2ä 2obb ob2e 2obe. 2obea ob3ein 2o3b4en oben3d4 
oben3se ober3in4 obe4ris 2obew 2o3b2i obi4t ob3ite 1obj ob1l o2b3li 2o3blo 
2o3bo o2b3re o3bri ob3s2h ob3sk obs2p ob2sta 2o3bu obu2s 2o3bü 2oby4 2oc o3ca 
oc1c o1ce och1a ocha2b o1che oche4b o2ch1ec och1ei ocher4k och3l och3m och1o 
och3ö2 och3r och1s ocht2 och3te o1chu ochu2f och1w o1ci o1ck o2ckar o3cke 
ock2er o3cki o2cko ock3sz o1cl o1ç o1d o3d2a od2dr o3deb o3d2e1i odein3 ode2n1 
odene4 ode3sp o3dex 2o3dia o3dir o3div o2don odo4s 2odr o2dre odt4 2o3du 2o1e2 
o2ec oen1 o4e3s o2e3t o3et. o3ets o1ë 2ofa of1a2c of1am of1au o2f1ei of2en 
o3fer of2f1a of2f1in 1offiz of2f5l of2f3r offs2 of2fu 2ofi of3l of1la of4lä 
of4lö 2ofo 2o1f1r of3ra of3rä of4rü ofs1a of4sam of2spe of2spr of2s1u 2oft 
of2tei of3th 2o1g o2g1ab oga3d og1ala og1ang o2g1ei oge2l1i o3gh ogi2er og2lo 
o3g4n ogs2 og3sp og1ste o1ha o1hä o1he o2h1eis ohen3s o2h1ert o2h1erz o1hi 
ohl1a ohl3au oh3lec ohl1ei oh3lem oh3len oh3lep oh4lerg oh4l3erh oh4lerw oh3lo 
ohls2e oh2lu 3ohng oh2ni 1ohnm oh2n1o o1ho oho2la oh1o2p o2h3ö ohr1a oh4rin 
oh1ro oh1s oh3t o1hu oh1w 2o1hy 2oi o1i2d o3ie o1im oimmu4 o1in oi2r o2isc 
o3isch. o1ism oiss2 oi1th 2o1j 2o1k oka2la okale4 3o2kel oki2o ok1lä ok4n 4okr 
ok2s1p okt4 2ol o1la o2lab o2l1ak ol2ar olars2 ol1auf o1lä ol4dam ol4dr ole3e 
ol1eie ol1eis oler2 ole3s ol1ex o1lé ol2fa ol2fl olf1r ol2fra ol2gl ol2gr ol2i 
oli3k4 ol2kl olk3r ol2kre ol2lak ol2l3au oll1e2c ol2l1ei ol2lel oll5ends 
ol4lerk oll5erwe o3lo ol2of olo3p2 ol1ort ol2str o1lu 3oly 1olym ol2z1a 
ol4z3ern ol2zin ol2zw 2om o2mab oma4ner om2anw om1art o2m1au o2meb ome3c o2m1ei 
o3m2eis o2mel o3men. o2mep o2meru om1erz om2es omiet1 o2m1ind om1ing o2m1int 
om3ma om1org om3pf oms2 omtu3 o4munt omy1 2ona ona2b o2nae o3nal on1ap o2narb 
on2au on3aus 2onä onbe3 2onc onderer5 2one one2i one2n3 onens2 o2n1erb o2n1erd 
on1erg on1erö o3nett on3f2 on3g2l ong4r ong3s 4o3ni on2i3d o4nikr o4n1im on3ing 
on3k2 onli4 onlo2c on3n2an on3n2e ono1 o3nod o2noke on1orc ono3s ons1a onsa4g 
on4sam on2seb onse2l onsi2 ons3l ons1p onst2h on3t2a ont3ant on4t3end ont3erw 
ont2h on4t3ri ont3s o1nu 2onuk on3v 1ony on3z o1ñ oof2 oo2k3l o1op o1or oor3f 
oo4sk oo2tr 2o1ö2 o1pa opab4 o2p3ad op3akt opa5s o1pec o1pei o1pe4n 2opf. 
op2f3a op3fah o2pfe op4ferd opf5erde opf1l opf3la op1flü 4oph2 o3phe o1pi 
opi5a4 opi3er. opi5ers. opin2 op5lag o2p3le op3li 2o3po op4pl op2pr 2o1pr 1opsi 
op3sz 1op3t4 o1q 2or. or1a or3a2b o1rad 2orak 2oral o2r3alm or4alt 3oram or2and 
o2ranh or3arb o1ras or3att o3rä or1änd or1ät or2bar orb2l or1c 2orca or2ce 
4orda or2d3am or2dau or4d3eng or2deu or2d1ir or2dit 1ordn or2do 2ordr 2ords 
ord3s2t or2dum 2ordw 4ore ore4as o2r1e2ck o2r1ef ore2h or1eig o2rein or1er 
o2rerf or1eth 2orf or2fle orf3s4 or3ga 2orget or3g2h 2orgia orgi1e or2gl or3gle 
or2gn 2orh 2o3ric o4rient o3rier 4oril 4orin1 2orit ork2a or2k3ar ork2s 2orm 
or4mans or4ment or5ne. or3n2o1 2o1ro oro3n2a 2o1rö 2orq 2orr orr4a or3rh 2ors2 
or3s4a orsch5li or3sh or3sz or2t1ak or4t1an or2t1au or2tär or2tef ort3eig 
or4t3ent or4t3ere ort3erf or2t3ev or2the ort3ins or4t3off or2tor or4tö or4trau 
or4t3räu ort3re ort3ric or2t1um o3ru or2uf o4r3un o2r3ü o2rya 2o3s2a os3ad 
os4an osa1s o3sche os4co 2o3se ose3e o2s1ei ose2n o4sents 2osh o3s2hi o3sho 
2osi o3sk o4ska os3ke o4ski 2os2kl 2os2ko os2lo 2oso 2os1p o2s3per o3s2po os2sa 
oss3and os4sä os2sei os4s3en4k os4s3enz os2s3o os4son os2s3p os2s3t ost1a 
osta2b os4t3am os3tarr ost4art os4ta4s os4tei oster3e os6t5er6we os2t3h os3til 
os3to os4t1ob ost3ran ost3rä ost3re ost3rot ost3uf 2osu4 2o3sy o3s2ze o2ß1el 
o2ß1en2k o2ß1enz o2ß1ere o2ß1erf 2o1t ota2go o5tark o2t1au ot3aug o2teb o3t2e1i 
otei4n ote2l1a ote4lei ot4em3 otemp2 o2t1erw ote2s 4ot2h ot4he ot5hel o4t3hi 
ot3hos o2thr o2t1i2m ot2in otli2 ot4ol ot1opf ot2or oto2ra oto1s o3tra o2t3re 
ot3rin ot2sa ot3sc ots1p ot4spa ots2pe ot2spr ot4terk ot2th ot2t3r ot4tri o3tü 
o2u oub4 ou2ce ou1f4l oug2 ou2ge ou3gl o3uh ou4le. o3um o3unds oun4ge. 2our 
ouri4 our4ne. ou3s2i outu4 2ouv 2o1ü o1v ove3s 2ovi oviso3 2ovo 2o1w o3wec 
owe2r1 o3wi o1x ox2a ox2e 1o2xid ox3l o2xu 1oxy o1y2en o1yo oy1s4 2o1z oz2e 
ozen4ta o3zi ozon1 órd2 ö1b öbe2la öbe4li öb2l ö2ble ö2b3r öb2s3 2ö1c öch1l 
ö2chr öch2s öchs4tu öcht4 ö1d ödi3 öd2st ö1e 1öf öf2fl öf3l ögen2s1 ög3l ög3r 
ö1he öh3l2e öh3ri ö1hu ö3ig. ö1ke ö2ko3 ök3r 3öl. öl1a2 öl1ei öl1em öl4en 
öl2f1ei öl1im öl1in öl2k3l öl3la öl2nar öl1o2 öls2 öl3sa öl3sz ö2l1u öl2ung 
ölz2w öm2s 2ön ön2e ö3ni önn2e ön2s ön3sc ön3sp ö1nu öo1 ö1pe öpf3l öp4s3t 
ör3a2 ör1c ör2dr ö2r3ec ö2r1ei ö2r1e2l ör2erg ö2rerl ö3r2erz ör2f3l ör2gl 
ö2r1im ör2kl örner2 ör1o2 örs2e ör3s2k ört2e ör2tr öru4 ö2r1une ö2sa ö2scha 
ö4sch3ei ö2schl ö2sch3m ö2schw ö2s1ei ö2sp ös2s1c ös2st ö2st ös3te ös2th ös3tr 
ö3su ö1ß 2ö1t ö2t3a öte4n3 öt2h öts2 öt2sc öt2tr ö1v ö1w ö1z öze3 özes4 p2a 
1pa. 1paa 1pac pa3da pa2dr pa2el pa1f4r pag4 pa3gh pa1ho 1pak pa1k4l pak2to 
1pala pala3t 1palä pa3li 2palt pa2nar pa3nei pa2neu pan3k4 2panl 3pa2no pan3sl 
pant2 3panz4 1pap papi2 papieren8 papie8r7end 3para pa2r3af par3akt 1parc 
pa5reg pa5rek 2par2er 2parg pargel6d 1park. par4kam par4kau par2kl par2kr 1paro 
2parp 1partn 1party par3z2 pa3s2p pa4st 2paß 1pat pat4c pat4e2 pa5t4r 1pau 
p3auf pa3uni 1pä 3pä2c pä3cke 3päd 3pär 3päs pä4t1e2h pä4t3ent pä2t3h pä2to 
pät3s4 2p1b 2p3c 2p1d2 pda4 p2e 1pe. pe2a pea4r pech1 1ped pe2en pef4 pei1 
2peic pe1im pekt4s 2peku 1pel pe2l3a4 pel3d pe2let pe2lex pe3li4n pe4l3ink 
pell2a pell4e 1pem pena4 pe3n2al pen3da pe4nen 1penn pe2n1o 3pensi 1pensu 
pen3z2 1pep pe1ra per2an pere2 1perl per4na 3pero pe2rob per2r1a 5pers perwa4 
pe3sa pes3s2 pe2st 3pet 1pé 4pf. p2fab p2fad p2faf pf3ai p2f1ak pf1ans p2fa4r 
pf3are p2f1au 4p3fe. p2fei pf1eim pf1ein p3fen. p2fent p3fer. pf2erw p3f2es 
pff4 p2f1in3s p2f3lä pf3lei pf3lie pf3lo pf3lu p2for pf3r pf1ra 2pfs2 pf3sl 
pf3sz 2pf3t 2p1g pgra2 1ph 4ph. ph2a 2phä 2phb 4phd 2p1hei phen3d phen3s 
2ph1ers 2phf 4phg phi2ka 4phk ph2l 2phm 2phn p3hop 2phö ph4r 2phs ph3t2 2phthe 
phu4s 2p1hü 2phz pi2a3 pias4 pi3as. pi3chl p4id2 piegelei8en pi2el piela2 3pier 
3pik 1pil pi3le pil4zer pin2e pingen4 ping3s 3pinse pi2o pi3oi pi3onu 3pip 
pi2pe pi3ri 3pirin 3pis 4piso pi3t2a pi1th pit2s pi2z1in p1j 2p1k2 pku2 pkur1 
1p2l4 2pl. 3p4la p5la. p5lad plan3g 3plä 2ple. ple1c p4leg p4lem 3ple5n4 2plig 
p4lik p4liz p4lo 2p3lu 2p1m2 2p1n 1p2o po3b4 po1c 3pod 2p3oh po2i po3id 3poin 
3pok 3p4ol po2lau po3li po4lor 2pond po1o2b po2p3ak po2p3ar po1pe po2pl po3pt 
po1ral po1rau 2porn por3s por4tin por4tre por6tri pos2e po4sta pos4t3ag po4stä 
po2s3te post3ei po2sto pos6tr post3ra po3ta 3pote po2t1u po2w po3x pö2bl pö2c 
2p1p p2p3a2b pp3anl ppe4ler ppe2n1 p2p1f4 p2p1h p3p2ho pp3l pp5lan pp1lä p2ple 
p2p3ra p2p3re p2pri pp3sa ppt2 p2r2 1prak 1prax p4rä 1präd 1präg 3präm 3präs 
2pre. 2prec 1pred pre2e1 1prei 3preis 2p3rer 3p4res pri4e 2prig 1prinz 1p4ro 
3prob 2proc 3prod 3prog 3proj 2pross pro1st 3prot 1prüf 2prün 2p1s 4ps. ps4an 
p3se p3s2h ps1id p2sö ps2po p2st p3sta p3stea p3stel p3s2ti pst3r ps2tu p3stü 
3p2sy ps2ze 2p1t pt1a pt2ab pt3alb pt3at p3te p4t3ec p4t1ei pte4l p4tele 
p4t1ent pt3erei p4t1erw p4t1erz p2th pt1in1 pto3me p4tos pto2w p2t3r pt3s2 ptt2 
pt1um pt1urs ptü4 3p2ty pt3z 1pu pu1a pub4 2puc pu2dr 2p1uh pul2sp 2pund pun2s 
2punt 2pur pu2s3t 3put put2s 1püf 2pül pün2 2p1v 2p1w pwa4r 3py1 pys4 py3t 2p1z 
qu4 1queu 1ra. ra2ab 2r3aac r3aal ra3ar r1ab ra2bar rab2bl 2rabd r2aber 2rabf 
2rabg 1r4abi ra2br 2rabs 2rabt 2r3abw 1raby ra1ce 2r1acet ra4cheb ra4chin 
racht3r rach6trä ra2chu r2ack r2ad r4ad. rada2 ra2dam 2radap 3radf 3radl 
r3a2d3r rad5t 1rae r2af raf3ar ra2fer ra3ge ra3gle ra2gn 3r2ahm 4raht 2raic 
rail4l 2r3air 1rake 3ra1k4l ra2kre ra2kro 2rakti 3rakü r2al r4al. ra2la2 ral3ab 
rala4g r3alar ral3b 3r4ald ra3le 2ralg r4ali rali5er. rali5ers ralk2 ral3la 
rall2e 2rallg 2r3alm. r3alp. 2ralpe r4als r3al3t r4alt2h ra2lu 3raly rama3s 
ra2mer 1r2ami r2amm ram4man ram6m5ers ram4m3u ram2p3l 2r1amt ramt4s r2an. 4ranc 
r4anda r4ande ran4dep ran4d3er rand3s 4r3anei r4aner 2ranf 1rangi rani1e ran2kr 
2ranl 2r1anm 2r1anp 2ranr r2ans. r2ansp ran4spa 2rantr 2r3anw r2ap 2rapf r1ar 
r2ara 2rarb 3rarei rar3f4 ra2r1in r2ark r2arp 2r3arz r2as r4as. ras2a ra4schl 
2r3asph 2raß 1rat r4at. ra2t1a r3atl rat4r rat2st 2r3atta 4rau. 3raub. 4raud 
rau3e2n 2rauf 2raug 3raum rau4m3ag rau4man rau2mi 3rausc 2rausg rau2sp 2raus5s 
raut5s 1raü r2ax 3r2äd 4räf 4räg 2räh 2räm 3rän. 3räni 3räns 2r1är r2är. rä3ra 
rä2s1c 3rätse rä2u räu2s räu5sche 4räut 2r1b r2b1ab r2b1a2de r2bak rbal3a 
rba3re rb1art rb1auf rbb2 rb1ech r4belä rb1ent rbe3r2e r3b2la rbla2d r8blasser 
r4b3last r3blä r2ble. rb3ler rb2lin rb2lö rb2o rb4ri rb2s rb3se rb4sei rb3ska 
rbs1o rb3sp rb4stä rb3str rb2u rby4t 2rc r1ce r1che. r1chen r1chi rch3l rch3m 
rch3r rch1s2 rch3sp rchst4r rch3ta rch6terw rch1w r1ci r2ck1 r1cl r1ç 2r1d 
r3d2ac r2daf r2d1ak r2d1al rd2am rdani1 rd1ant rd1anz r4dap r2dei rd2ei. 
r2d1elb r3den rden3d rden4gl rde3re rder4er rderin6s r4d3ernt rde3sp rdi3a2 
rdia4l r2d1inn rd1it rdo2be r3don rd1os r2dö rd3rat rd4ri rdt4 rd3ta rd3th 
rdwa4 1re 3re. re3aler re2alt re2am re3as re3at. re3ats 2reä re2b1a re2b1l 
reb1r reb3ra re2bü r2ech rech3ar 4rechs 2reck. 2recki 4redd 2redit re1el re1er 
3refe 4reff 3refl 3refo 3reg 5reg. rege4l3ä re2hac re4h3ent re2h1i rehl4 re2h1o 
r2ei. rei4bl r2eie 2reig 3reigew rei3l2a rei3l2i reim2p r1ein rei3nec 4reing 
r3eink 4reinr rein8s7tre re1in2v reister6 3rek 4re2ke re3la 2r1elb rel2e re3lei 
2re2lek 2r1elf re3lo 2r1elt relu2 r4em. r2emi 4rempf 4remu r4en. r2ena rena2b 
re3nal re2nä 3rendi ren3dr re4n3end ren4gl 2rengp re2ni r1ense 2r1entl 2r1ents 
2rentw 4r3entz r2enz re3or 3repe 3repo 4repp 3r4er. 2r1erb r2erbr 2r1erd r1erf 
r1erg r4ergen r1erk 4r3erken r2erki r1erl 4r3erlau 2rerlö 2r1erm rer2n 2r1ernä 
4r3erns 4r3ernt r2ero re2rob r1erö 3r2ers. 2r1ersa r2erse 2rersp r1ert r2erte 
2rertr 2r1erz rer5ze r2erzy 3r4es. re2sa 3rese 3reso 2ress ress2e res6s5erw 
3rest re1sta re2s2tu 3resu re2thy re2u reu3g2 2reul re3uni 2r1eur 2reü 2r3evid 
r1ew rewa4r re2wi 2r3e2x1 3rez 4rezi 1ré 2r1f rf1ält rf2äu r2fent rf2es rfi4le. 
rf3lic rf3lin rf4lö r3flü rfolg4s r3for rf4ru rf4rü rf2sa rf2s1ä rf4s1id 
rf2s3pr rf2s3t rf2ta rf3t4r rf2u 4r1g rg2ab r2g1a2d r2g1ah r2g1ak rg2an rge4an 
rge2bl rge4l3er rgen4z3w rge4ral rge4tap r2geto rgi4sel r2glan r2gleu r2glig 
r2gno r2g1ob r2g3ral r2greg r2gres r2gret rg3rin rg3s2p rgs4tr rg5s2tu r1h4 
2rh. 2rha r2ha. 2rhä 3r4he. 3r4hen r3her r2hoe rho2i3 2rhol 2rhö 2rhs rhu2s 1ri 
ri3am ria1s ri3at rib2bl ri1ce ri1cha rid2 ri2d3an 2ridol r2ie rie2fr ri1el 
riene4 rien3s rie2nu ri1er. ri4ere ri3ers. ri3esti ri1eu ri2f1a ri2f1ei ri2fer 
ri2f1o ri2fr rif3s rif4ter 3rig 5rig. 5rige ri4gene 5rigj rig1l 4rigr rik1l 
ri4kla r2imb 2rimp rim2s rim4sc r2i3na 2r1ind rin4dex rin4diz ri3n4e rine1i 
2r1inf rin2fo ring3l rin2gr 2r1inh 2rinit 2rink 3rinn 6r5innenm 4r3inner 
4rinnta r1innu 2r1ins 3r4ins. rin4so rin2sp r4inspi 2rint rin4teg rin4t5r r1inv 
r2inva 2rinve 4r1ir r2is ris2a ri4scho ri4schw 3risik ri3so ri4s1p 3riss ri2st 
ris6t5ers r2it r3i2tal ri3t2i rit4r rit2tr 5ritu rix1 1rí 2r1j 2r1k rk2am r2käh 
r3klau r2klis rk4lo rk2lu rk4n r2k5nu rk3räu r2k3rea r3kri rk3rin rk2s1e rk3shi 
rk2sp rk1st rkstati6 rk4stec rk2ta rk4t3eng rk4t3erf rkt3ers rk6tersc rk4t3erw 
rk2tin rk2t1o2 rk2t3r rk3tra rk4tri rk1uh rk2um rku2n rk1uni 4r1l r3l2a rl2e 
rle2a r3lec rle2i r3let r3l2i rli2s r3l2o rl2ö rlös3s rl2s1p rl3ste rl2s3to 
rl3t 4r1m r3m2ag rma2la r2m1ald rm1ans rm1anz rm1a2p r2maph rm2är rm3d2 r3me. 
r2m1ef r2meo rm2es r2mide r2m1im r2m1o2ri rmo1s rm3sa rm3sta rmt2a rm2u rm3ums 
4rn rna2b rna4n rn2and rn3ani r2n1anz rn2a2r rn3are rn3ari r2nau rnd4 rn3dr 
r3ne rn3e4ben r4nef rn2ei rn3eif r4n3eis rne2n r4n1ene rn3ense r4nerf r4n1erg 
rn4erhi r4nerk r4n1ert r5nes rn2et r4nex rn3f rng2 r3ni r4n1in r3nod r2n1op 
r2n1or rn1ö r1nöt rn3s2ä rn3s2p rn3s2z rn3t2e r1nu rn1ur r1nü r1ny ro2bei 2robj 
3robo 2robs ro1c 3rock. r2o3de ro3e4 2rof roh1l roh3na 3r2ohr 3roi ro1ir ro3le 
rol4lan rol3l4en rol3s 2roly 4rom. ro2mad ro2mer 4romm 4romt r2on 3ronn rons2 
ron4tan ro1ny ro1pe ro3ph r1or r2ora ror3al ro2rat ro2rei ro2r1o ror3th ro3sh 
ro3s2i ro3smo ros2p ros2s1c ro3st2a rost1r 4roß ro2ßu ro4tag rote3i ro2tho 
ro4tri rots2o rot2ta ro3t2u ro3unt 3rout 2rox rö2b3l rö2du 2röf 4rög 1r2öh r1ök 
1r2öl 3römi 4röp r1ör r2ös. r2öse 2r1p2 rp4a rp4e rpe2re rpe4r3in rpf4 r2pli 
r3po rpro1 rps3t rp3t r3pu r1q 2r1r rr2ab rr2ar rr1äm rrb2 rr1c r3r2e rre4ale 
rrer4s rre2st r4rew rr2he rrik2 rr2n3a rr2o r2r3ob rro3m rr2st rr3stu rr2th 
r3ru r3r2ü rrü1b 4r1s rs3ab r2s1a2d r4samp r4s1amt rs2an r2s3ang rs3anp rs3ant 
rs3ar r3sch2e r6scherl rsch2l r3schu r3schw r2sein rse2n1 rs2end rse4ne rs1ere 
rs1erö rs1ers rs1erz rs1eta r3sho r3si rs2kal rs2kan rs2kie rs2kis rs2kl r4sko 
r4skr r4sku rs3l rs4no r3so r4sob r4s1op r4sord r4s3ort. rs2p4 r2s3ph rs3s2 
r4stant rs2tec r6st5eing rs4temp rs4terb rs4t3er4w rs2th rs2ti r3stie r2stin 
rst3ing r2stip r3sto rs4tob r4stot r3stö r3s4tr rst3ran r6strang rs2tu r3s4tü 
r3swi r3sy 4r1t rtal2 r2t1alm rtals1 rt1am rt1ang rt1ann rt1ant rt1anz r2t1ar 
rt3a4re r2t3att rt1är rte1e2 rt4eif rtei3la rtei1s4 r2telf r2temo rte2n1 
rten3s2 rt3erei r4terfo r4t3erh r2t1erk r4t3er4la r4t3erle r4t3ernä rter4re 
rt1ers rte3s2k r2thi rt3hol rt2hum r2t1id r2t1ima r2tinf rto1p rt1or rto2ri 
r3tö r4trak rt3rec r4treis r5tri rt1ros rtrü2c r4ts rt4s1eh rt2so rt2spa rt2spr 
rtt4 r2t1urt r3tü rt3z 1ru ru1a ru3a2r3 rube2 ruch3st ru6ckerl ru2cku rude2a 
ru2dr 3ruf ru2fa ruf2s3 4rug 2r1uhr 3ruin ru1ins ru1is 2rum 4rumf ru2mi 4ruml 
r2ums. 4rumz 2r1una 2rund run2d1a r2unde rund3er run6derl run6ders run6derw 
2r1unf 2rungl 2r1u2ni 4r3unio run2kr 2r1unl 2r1unm 4runn 4r3unt 2runw ru3pr 
4r3ur ru2ra ru2r1e 5ruro ru2si rus2s1p rus4st ru2st ru3sta 3rut rut3h ru2t1o2 
ru2t3r 4ruz ru2zw 1rü 2rüb rü1ben rü1ch 4rümm 2r1v rve4n1e 2r1w rwun3s 4r1x 1ry 
ry2c 2r1z rz1a2c rz2an r2zar r2zas r5zene rz1eng r4z3ents r2z1erf r2z1erg 
r2z1erk r2z1erw rz1id r3z2of rz1op rz2ö rz3te rz2th rz2t3ro rzug2u r3zwä 
r3z2wec 1sa 3sa. 3saa 2s1ab sa2be 3sabet sa2bl sa3ble sa2br 4sabs sa2cho2 
sach3t 2s1ada s1adm 2s1a2dr 3safa sa2fe 2s3aff 3safi sa1f4r 3saga sa4gent sag4n 
sa2gr 3sai sa3i2k1 sail4 2s1ak sa2ka 3saki 3sakr 4sakt 3s2al. sa4l3erb sa2l1id 
3salo sal2se 2s1alt 3s2alz 3sam s3ameri 5samm 6s1amma 4s1amn s1amp sam2to s1an 
s2an. 2s3a2na s3anb s2an2c s2and s4and. san4dri 3sang. 2s3anh 3sani 2s3anl 
2s3ans san4sk 4s3antr 2s3anw 2s1ap sa2po 3sapr 2s1ar 3s4ar. 3s2ara 4s3arb 
3s2ard 3sari s3arr 3s2ars 4sarti s1asp 4s3a2sy 3sat sat2a 4s3ath 4s3atl 4satm 
sa2tr sa3ts sat4z3en s1a4u 3sau. 3sauc 3saue 2s3aufb sau2gr 3saum 3saur sauri1 
2s3ausb 3s2ause s3ausw 2s3av sa2vo 1sä s3ähn 3säl s1ält 2s1äm 2s1änd 3sänge 
2s1är 3s2ät 3säul 2säuß 4s3b4 sba4n sbe3r2e 1sc 2sc. 2scam s2can s2cap 2scar 
2s1ce 6sch. 2schak s4ch2al 4schanc 4schang 2schao s4chä 4schb 4schc 2schd 
3sche. 2schef sch3ei. 4schemp sch2en 3sches 4schess 4schex 2schf 2schg 2schh 
schi4e s4chim 4schiru 3schis 2schk s4chl 4schle. 6schlein sch6lit 2schmö 2schn. 
2schox s4chö 2schp 2schq 4schre. 4schrin sch3rom 4schrou 6schs schs2e sch3s2k 
4sch3t scht2a scht4r s4chu 4schunt sch2up 3schü 2schv 4schwet sch4wil 2schz 
2scj 4s3cl 2sco 3s4cop 3sco4r s2cr 2scs 2scu 4s3d2 sda3me sde1s sdien4e sd4r 
1se se3at. 2s1e2ben seb4r 2s1echo s1echt 2s1e2ck 3see se1ec se2e1i4 see3ig 
seein2 se1er. se1erö 2s1eff se2gal se2gl seg4r 3seh se2h1a4 se3he se4h1ei 
se4hel se4herk se2hin seh1l seh3re seh1s seh3t se2hüb 2s1ei. 2s1eig s1ein 
5s4ein. 2seinb sein4du sei3n2e sein4fo 4seing 2seinh 4seink 2seinl 2seinn 
4seinr s4eins. 4seinsp 4seinst 2seinw 4s1eis 3s2eit 3s2ek s2el. se2l1a se3lad 
sela4g se3lam sel1ec 4selem se4l3erl sel3ers 2self. s3elix se2l3ö s2els sel3sz 
sel3tr s4e3ma 2s1emp 3s2en. se4nag se2nä 2s1endl sen3gl 3s2eni 3senk se2no 
se4nob 3s2ens s2ent. 4s1entf 2s3entg s2enti 2s1ents 2sentw 2sentz se2n3u seo2r 
4s1e2pos 3seq s4er. 3sera ser3a2d se2r3al se5ref s3ereig 6sereign se4r3eim 
se4r3enk ser2er 2s1erfo s2erfr s3erfü 4serfül ser3g s2ergr s1erh 2serhö 3seri 
4serken 2s3ernt se2rob 4s3eröf s2ers. 2sersa 4serseh s4ert. s2erta seru2 
se4r1uf se3rum se3rund 3s4erv 5ses. se2sel se1sta se3su 3set 4se4tap se2tat 
4s1e2th se1u2n 2s1ex se2xe 4sexp sex3t 1sé 4s3f4 sfal6l5er sflo4 4s3g2 2s1h 
sh2a 3s2ha. sha2k 4s3han 1shas s3hä s3h2e 3shi. 3shid shi4r sh3n s3hoc 4shof 
3shop sho4re 3show s3hö sh4r 1si si2ach si3ach. si2ad si3am. 2siat sib4 5si1c 
2s1i2deo s2ido 3s4ie siege4s sien3 si3ene si1err sie2s si1f4 3s4ig si2g1a2 
sig4n si3gnu si2g3r sig4st si2k1ab si2k1ä sik3erl si2ki si4k1l si2kr sik3s 
sik3t4 si2ku 3silo 2s1imm si3n4a 2s1ind 2s1inf sing1a sin3gh sin3g4l sin2gr 
sing3sa 4s1inh sin1i sini1e 2s1inq 2s1ins 2s1int 4s1inv 3sio sion4 3s2is si2sa 
si4schu si2s1e si2s1o si2s1p sis3s 3s2it si2tau sit3r si2tra si3tu siv1a sive3 
si2vr 1sí 2s1j 2s1k2 4sk. 3skala 4skam 4skanz s3kar 4skas ska4te. 4skateg 
ska4tes 4skb s4kep 3s2ki. s2kif s2kig 3s2kik 4skir ski1s 3skiz sk4l 4s3klas 
sk4n 4skom 4skor 4skow 4skö 4sks 4sk3t 3skulp 2s1l2 3slal 4slan s2law s3lä sl3b 
s3le sler3s s3li 3s4lip sli4tu s3lo. slo3be s3loe 2s3m2 2s3n4 4sna snab4 
sni3er. sni3ers 4s5not 4snö 1so 3so. so4a 2s1o2b so1c so3et 3soft 3sog s1o2he 
4sohng 2s1ohr 3sol so3la so4l1ei sol4ler 4so2ly 3som 3s2on son3au sone2 
son5ende son3sä so2ny so3o 2sopf 3sor. so1ral s1orc 2s3ord so2rei 2s1orga 
5s2orge 2s1o2rie so2r1o2 3sors so4ru 3sos s4os. 4s1ost so3unt 3sov 4s1o2ve 3sow 
2s1ox 3soz 1sö sö2c sö2f 2s1ök 2s1ö2l s1ös 1sp2 2sp. 2spaa 2spak s2pan 
spani7er. 2spap 2spara 2sparo 3sparu 3spaß 2spau s2paz s2pä 3späh 2spär s2pee 
2spel 4spensi spe3p4 2s1peri 2sperl s2perr 2spers 2spet 3s2pez 4s3pf 2spha 
s3phe 2sphi 3s2pi4e 4spier4 spi2k 4spil 3spio 4spip 4spis 2spl 4spla 4splä 
3s2pli s3p4lu s3pn 2spod 2spog s2poi 2spok 4spol 4s3pos s2pott 4spr. s2prac 
s2pran 2sprax 2spräm 4spräs 3s4prec 2spred 2spres 2sprob 3spross 3spru 2sprüf 
2s3ps 2spt 2spun 2spup 3spur 4sput 4spy 2s1q 4s3r4 srat2s srat4sc sret3 srö2s1 
srücker6 srü2d 6s1s ssa3bo ss1a2ck s5saf s3sag ss1aj s3sal s4s1ala s4s1alb 
s4s3amt s4s3ang s2sano s4sans ss2ant s4s3anz s3sa1s2 ss3att s3s2ä s4sce s4sco 
ss1ec s2s1ega sse3ha sse3inf sse3in4t sse6r5att ss1erö ss3erse s3s2es sse3ta 
ss3l ss1off ssoi4 s2s1op ss1ori ss2po s2spro ssquet4 ss3s4 sst2a s3stel ss2th 
ss2ti ss4tip ss2tur s3stü ss1ums s1t 6st. s2ta 4sta. 3staa 2stabb st2ac 3s4tad 
3staff 2stag 3stah 2stak 2stale s3ta3li 2stalk st1alp st1ami 4stan. sta4na 
3stand 2stani 4s3tann 2stans 2stanw s4tar. 4stari s4t2ars s3tat. s4tau. 2stauf 
2staum 3staur 2staus 3staus. 2stax 3s2tä 4stäg 4stält s4tänd 5stätt s3täus 2stb 
2st3c 2std st2e 4s5te. 2stea 4stechn s2ted 4stee 3s2teg ste2gr 3s4teh s2te2i 
3steig 4steil 3steilh stei4na 1s2tel 2stel. stel4l3ä 2steln 2stels 2stem 4stem. 
ste4mar 4sten s5ten. s4t3ends s4t3engl st4ens s4t3entf s2tep 2ster 6s5ter. 
ste6rers 4sterm 3sternc 4stes s4t3ese stes6se. ste4st 2stet s4teti 3s4tett 
3s2teu 1steue 4steuf st3ev 4stex 2stf 2stg 4sth s4thä s4thi s2t3ho s2thu 2stia 
2stib s2tic sti2e 2stie. s2tieg s2tiel 2stien 3s2tif 2stig 2stik s2til 3s4tim 
s4tinf s3tinn st1ins 2stio 1s2ti2r 2stis st1i4so 1stitu 2stiv 2stj 2stk 4stl 
4stm 2stn s2to 2sto. s3tob 2sto3d 4stod. 1stof s4toff s4t3om 4ston 4stoo 2stopo 
2stor. 2store 2storg 2stori s3tort 2stose sto3s2t 1stoß 4stote 4stou 2stow 
2stoz 1stö 2stöch 2stöt 2stp 2stq s2tr 2strad 2strag 1s4trah 4strai 4strak 
2stral 4strans 3s4tras 5straß 4straum 4s5träg 4sträne 4s5tref 4streib 5st4reif 
st3renn 2s4trig 1s4tri2k 2s5tris st3roll stro4ma 1stru 2strua 2strug 3struk 
4st3run 2strup 2s4t3s4 2st3t4 st2u 1stub 4stuc 3s4tud 2stue 3stuf 3stuh 2stum2s 
stum4sc 2stumt stu2n 2stun. 3s4tund s2t3uni 4stunn 2s3tuns 2stunt stu3re st3url 
2sturn 2st3urt 2s3tus 1stü 2stüch 2stür. 2stüre 2stürg 2stürs 3stüt 2stv 2stw 
3s2tyl 4st3z 1su su1an 3su2b3 su4ba2 4subi 3su1c su2cha such4st 2s1u2f 2s1uh 
su1is su1it. sul2a sul2i sult2 su2mar su2mau 3s2ume su2mel su6m5ents s3umfe 
3summ sum1o2 su2mor s3umsa s3umst su2n 3sun. sun6derh su4ne s1unf 2s1uni 4sunt 
3s2up sup3p su2ra 2s1url s1urt s4u2s1 su3sa su3sh su3si sus3s 3suv 1sü 2sü4b 
3süc sü2d1 süden2 3sün 4s3v 2s1w s3wa s3we sweh2 4swie 4swil 1s4y syl1 sy4n3 
2s1z 4s3za 4s3zei s2zena 3s4zene 4szent s2zes 4s3zet s2zis sz2o 4s3zu s3zü 
4s3zw 2ß1a2 2ß1b2 2ß1c 2ß1d 1ße 2ß1ec 2ß1e2g 2ß1ei ße2l1a ßen3g ße2ni ße2no 
ße2ro ß2ers. 2ßerse ßer3t 2ß1f 2ß3g2 ßge2bl 2ß1h 1ßi ßi2g1a2 ßig4s 2ß1in ß1j 
2ß1k4 2ß1l ßler3 2ß1m 2ß1n2 ß1o2 ßos2 2ß1p2 2ß3r2 2ß1s2 ßst2 2ß1t 1ßu 2ß1um 
2ß1ü 2ß1v 2ß1w 2ß1z 1ta 3ta. 4taa 5taan 4tab. ta2b1an 2t1abb 3tabel 2taben 
ta4bend 2tabf 2tabg 2tabh 2tabk 3table 2t3abn ta2br 4tabs 2t3abt ta2bü 2tabw 
2tabz 2t1ac 3tacu t1ada tadi3 2t1a2dr ta3d2s 3taf. 3taf2e 4taff t1afg t1af4r 
3t2ag ta2ga2 ta2g1ei 4t3a4gent 4ta3gl t3ago tag4st tah2 tah3le tahl3sk ta3i2k 
tai2l ta1ins tai4r ta1ir. t1a2ka ta2kro tak6ta 3taktb 3t2aktu 2takz 3t2al. 
ta2la ta3lag ta3lak tal3d 3t4ale ta4lens tal2lö 3talo ta2l1op 2talt 2tam 3tame 
ta2mer ta2mi t1ampl t1amt 3tan. t1a2na 2tanb 4t2and ta3ne 4tanf 2tang 3tani 
t2ank t3ankl 4tanl 2t1anme 4t1anna t2ano t1ans 3t2ans. 4t3ansi 4t3ansp ta2nu 
2tanwa 2tanwä t2anz. t1anza tan6zerh t1anzu ta3or ta2pe. ta2pes 2tapf ta2pl 
2tarb ta4rens ta4r3ere 3t4a3ri 4tark 2t1arm 2tart t1arti tar2to ta2ru 2t1arz 
3tas ta3sa 4t1asp ta2ta2b ta2tan ta2tau tat3ei ta2tem ta2t3er ta2th tat3he 
t3atl t4atm ta2tom 4tatue ta2t1um 2t1auf 4taufg tau3f4li 4taufn t1auk 3taum 
t1ausb 3tausc tau6schr tau6schw t2ause 4t3ausg t1ausk 4tausl 4t3auss 4t1ausw 
3tav 3tax taxi1s 1tä 4täb tä1c 4täd 3täe 3täg 4tägy 2täh 2t1ält 4täm t1ämt 
t1ängs 3tänz t1äp t2är. tä2ru tä2s t2ät 4tätt 2täuß 2täx 1tà 4t3b2 tbe3r2e 
tblock5e tblocken8 4t1c t3cha t3che tch2i tch3l t2chu tch1w t4ck t3cl t3cr 
4t3d4 tdun2 1te 3te. te2a2 2teak te3al te3an 3teba 3t4ebb 4t1e2ben t2ech te3cha 
3techn 2teck teck2e te2cki te1em te2en3 te1erw te2es 2teff teg3re 2teh 3teha 
3tehä 3t2ei. t2eie t3eifr teik4 3teil 4teilhe 2t1ein tein3e4c t3einge t3einla 
4teinn t3eis. t3eisb 5tel. 3tela te2l3ab te2l1ac te2l1au telb4 3te3le tel1eb 
tele4be te4l1ec te4l1eh te4lein 2telem tel1en te4lerd te4leu 4t3elf. 3telg 
te2l1in te2lit 3telk tell2e 5teln te4lost te2l1ö 3telp 5tels tel3s2k 3telt4 
tel3ta tel3th 3tem. te2m1ei te2min 2temme te2m1o2r 3temper 2tempf tem3s te4m1u 
3ten t6en. ten3a tena2b te4na2d te4na4g te4nas te4nau te2nä t4enb ten3da 
4t3endf t6endi 4t1endl t6endo 4t3endp ten3d4r te2n1e2b te2nef te3n4ei. ten3eid 
ten3ens 4tenerg te2net ten3g 4t1eng. ten4gla t4enh te2ni te4n3in t4enj t4enm 
ten3n tens2e 4tensem t4enta t3entb 4tentd t4ente 4tentn tent3ri 4t3entw 4t3entz 
ten6zerh ten3zw t3e2pi 3t4er. tera2b te1raf ter3am te3ran. 4terbs 4terbt 3terc 
4t3erde. te2re2b te4r3eif te2rel ter3end te4reng te4rerk terer4z 4terfol t4erfr 
4terfül 3ter3g2 6tergrei t6ergru t4eri te3ria 4terklä 2t1erlö ter4mer 3termi 
ter4n3ar 2ternc t3erneu t4ero t3erö ter4re. t4ers. t6erscha ter4ser terst4 
t4erst. t4ersti t4erstu tert2 teru2 te4r1uf ter4wäh 6terwerb ter3za 2t3erzb 
3tes tesa2c te2san tesä2c te2sel te2spr tes3s2 t2est tes3tan test3ei tes6ter6g 
tes6terk testes4 te2su 3tet2 t2et. te2tat 4teth 4tetl teu3ere teu3eri 3teuf 
3teum te1un 3teur. teu2r3a te2vi te1xa 2t3e2xe 2t1e2xi 4texp 3text 2t1exz 4t1f4 
tfi2l 4t1g2 tger2 t1h 4th. 2th4a 3t4ha. t2hag t3hai t2hak 3thal. 4t3hau 2t3hä 
th2e 1t2he. 3thea 2theb t2hec 2t3hei t4hein t2hek t2hem 1then t4hene t4heni 
3theo 2therr t2hes 3these t2heu 1thi t2hik 2t3hil 2t3him 2thk 4th3l 4th3m 2th3n 
1t2ho 2t3hoc t3hof 2t3hoh t4hol. t3hor 2t3hot thou2 4t3hö 2thp 1th2r2 4thrin. 
4thrins 2ths 2thub 4thun 2thü 2thv t2hy 1ti ti2ad ti3a2m 3tib4 ti1ce tiden2 
ti4dend ti2deo 3tief. tieg4 2tieh ti1el ti3e4n3 3ti2er tie4rec ti1et ti1eu 
3tif. ti1fr 4tift 3tig ti4gerz 3tik ti2kam ti2kar ti3k2er ti2kin ti2krä ti2lar 
ti2lau ti2lei ti2lel 3tilg ti2lö til3s tilt4 ti2lu ti2ma2g t2imi tim2m1a 4t1imp 
3t2in. ti3na t1inb 4t1ind ti3n2e t1inf tin2g1a ting3l ting3s t1in1it 2t1inj 
tin2k1l 3t2ins. 4t1inse 2t1int ti1nu 4t1inv 3tio ti3or 3tip ti3pl ti4que. ti1rh 
3tis ti4scha tisch3w ti2sei ti2sp ti1sta 3ti3t2e 2ti3tu tium2 3tiv ti2van tive3 
ti2vel ti4v3erl ti2v1o ti2v3r ti2za 2t1j 4t3k4 4t3l tl4e tle2r3a 6t5li tlung4 
4t3m2 tmal2 tmen6t3 tmo4des 4t5n4 tnes2 tnes4s 1to 3to. to4as to5at 4tobj tob2l 
to1c 3tocht to6ckent 3tod tode2 4to2d1er to4d1u toi4r 3tok to3la 3tole 4tolz 
tom1e2 to2men 2tomg 3ton to2nau 3too to2pak to2pat 3topo 2topt 3tor. to1ra 
to2rau to4rän 4torc t1ord 3tore to2rel to3ren t1org t3orga 3torin tor3int to2rö 
3tors t1ort. to2ru t2orw to3sc 3tose to4sk tos2p 4toss 3tost4 to1sta 4toß 
3to3te to2tho 3totr tots2 3t4ou touil4 to3un 3tow 2tö 3töch 4töf 4t1ök tö4l 
3tön t1öst 4töß 3töt 4t3p2 tpf4 2t1q 1t2r4 2tr. 5tra. 3trac tra3cha 4tract 
t3rad. tra4dem tra4far 3trag 6trahm 5t4rai 3trak 3tral 3t4ran. 2trand 3trank 
t3rann 3trans t3rase t3rasi 4traß 5träc 3träg 3träne 4träs 4träß 4t5re. tre4ale 
4treb tre2br 4trec t3rech t4reck 6t3red 5t4ree 3tref 4trefe 4trefo 4treg t4rei. 
3t4reib 4treic 2treif t3reig 2t3reih t3rein t3reis 6treit t3reiz 2trek 6t3rel 
t4rem t4ren. 3trend 4trendi t3rent 2trepe 2trepo t4repr t4rer t4res. t4ret 
tre2t3r t4reu 3treuh t3rev 2trez 5t4ré 2t3rh 3tri 4tric 2trid 5trieb tri4er 
5trigg t3rind 4tring tri3ni 4trinn t4rip 4tript tri2x trizi1 3tro. 3troe 3t4roi 
tro2ke 4trom. tro2mi 4troml 3tron 2t3roo t4rop 3tropf 3troy t3röc 2tröh 3trös 
2t3röt 3trua 4truk trum2 trums1 2trund 3t4runk 5t4rup tru2th t4rüb trü1be 
trü1bu 2t3rüc trücker6 t4rüg try1 2ts 4ts. t4sa4b t3s2ac ts1ad t2s1ah ts1al 
t4s1amt4 t2san t4s3ar ts1as t2sau t2s1än t3s2cha t4schar t3sch2e t4schef 
ts4chem tsch4li t4schro ts4cor t2s1e2b t3seil t4seind ts1em tse2n1 t2s1eng 
t2s1ent t2s1er t4s3esse t2s1i2d ts1ini t2s1ir ts3kr t1slal ts1o tso2r t3sou 
t2sö t3spal ts1par ts4pare t2spä ts2ped t3spek t2sph t3s2pi t2spo t3s2pon 
t3s2por t4sprei ts3s4 t1st4 t4stag ts3tak ts4tal ts3täti t2s3tep t3s4tero 
t2stip t4stit ts3toc ts3tor ts3trad t4stran ts3trau t2s3trä t4streu t2stri 
t4strop t2s3trü ts2tu t2s1u 1tsub t3sy 4t1t tt1ab tta2be tt2ac t2t1ad tta6gess 
tt1ak tt2al tt2ant tt1art tta1s tt1ebe tt1eif tt1eis t3tel tte2la tte4leb 
tte4len ttel1o ttes1 tte2sa tte2sä t4teti tt2häu t2t3ho t3ti t3to tto1s t3tö 
t3tro tt3ru tt3rü tt2sen tt2sor tts1p tt2spe tt2spr tt2sti ttt4 t3tu tt2un t3tü 
1tu tu1alm tu3an 2tub 3tuc tu2chi 2tud 3tue 4tuf tuf2e tu3fen t3u2fer tuff3 
2tuh 2tuk t3u2kr tul2a t2um. 3t2ume 2t3umf 2t3umg 2t3umk 2t3umr tum2si tum2so 
tums5tr 2t3umt 2t3umz 3tun. 2t1una 2t1und 3tune 2t3unf 3tung t3unga tung4s5 
2tunif 2t1u2nio 2t3unt t1up. tu2r1a4g tu2rä tur1c tu2re. tu2rei tu2r1er tu2res 
tu2r1e4t turin1 3turn tu2ro tu4ru tu2sa tu4schl tu2so tu3ta 2tü 4tüb 3tüch 
tück2s 3tüf 3tüm 3tür. tür1c 3türe 3türg 3tür3s 3tüten 4tütz 4t3v 4t3w twa2 
twi4e 1ty1 3typ ty2pa tys4 4t1z t2za4 tz1ag tz1al tz1ar tz1au tz1ä t3ze. 
t2z1e2c t2z1eie t2z1eis tze4n1 tz2ene tz3ents tz1erl tz2ers t3ze2s tzgel2 
tz1ind tz1int t2zor tz2ö tz2th tz2tin tz1wä tz1wi tz1wu 2ua u1a2b u1a2c uad4r 
u1al. ua2lau u1alb u3alet u1alf u3a2lo u1alr u1als u1alt ua2lu u1am u1ans u3ar. 
uara2b u1ars ua3sa ua2th uat2i u3au u1ay u1äm u1äu 2u1b u2be2c u3b4i ubi3os. 
ub2l ub3lic u2b3lu u2bop ub1r ub3rä u2b3rit ub2san ub2s1o ub2spa u2büb 2uc uc1c 
u1ce uch1a u1cha. uch1ä u1che u2ch1e4c uch1ei u3ches u1chi uch1il uch1in uch3l 
uch3m uch3n u2ch3r uch2so uch4spr uchst4 uch4tor uch2t3r u1chu uch3ü uch1w u1ci 
u2ckem u4ckent u3ck2er u2cki u1cl 2u1d u3d2a uden3s2 uder2e udi3en uditi4 u2don 
ud3ra u3dru 2u1e ue2ck u2ed ue2en u2eg u2ela ue2le ueli4 ue2mi uen1 ue2nä 
ue2ner uenge4 ue2ni ue2no uen2zu u2ep ue2r3a ue2r1ä u2ere u3ereh ue3reig u3erer 
ue4rerg ue4rerk u3erex uer3g2 u4erinn u3erin4t uer2ne uer4ner uern3s4t ue2r3o 
u3err uer3sc uer3t2 u3erum u3erunf u3erunt ue2ta ue4tek u3fah uf1ak uf3ar u3fas 
uf1au u2f1äs u2f1ä2ß u2f1ei u2f1em u3fen. u2fent u2f1erh u4ferle uf2ern 2uff 
uff4l uf2fro uffs4 uf3l u2fob ufo2r uf1ori uf3r uf3sä uf4sin uf4so uf2spo 
ufs3tem uf2t1eb uft3s2 u2fum 2u1g u4gabte ug1af ug1ak u2g1ap uga4s ug1au ug3d2 
u2g1ei u2g1erf u2g1erl ugge4st ug3hu u2g1l ug3lad ug3lo u3g2lö u4glu u2g3n ugo3 
ug1or u2gö u4g3reis ug3ro ug3rüs ug3se ug4ser ug3si ug3spa ug4spr ug4spu ug5stä 
ug3str ug3stü u2gü u1h 2uh. uhe3s6 uh1la uh1lä uh2li uhme4 uhr1a uh2rer uh3ri 
uh4rin uhrt4 uh2ru uh4rü uh1w 2ui ui2ch u1ie ui1em u3ig u4ige u1in. u3isch. 
u3ischs uisi4n ui4s5t u1j uk2a u3käu u1ke u1ki u1k2l ukle1i uk4n uk2ö u1k4r 
uk2ta uk2t1in uk2t3r u1ku uku2s u1l ul1ab ul1am ula2s ul1äm ulb4 ul2dr uld2se 
u2l1el ule4n ul1erf ul1erh ul1erw ule2sa ule2t ul1eta u2lex ul3f4 ulg4 uli2k 
ul1ins ul3ka ul2kn ull2a ul2les ull3s ulm3ein ulo2i ul1or ul2p1h ul2sa ul4sam 
uls2th uls3z 2ulta ul3th ul4tri ult3s u2lü ul2vr ulz2w u2m3a2k um1all um1anz 
u2m1art u2m1aus u2maut 1um3d2 um2en ument4s umer2a u2m1erg u2m1erl u2m1erw 1umf 
1umg um1ins um1ir 1umk 1um3l 4umm umm2a umpf4li um2p3le 1umr 3umsat um4ser 
um2sim um2s1pe um2su um3t2 um2un u2m1ur 1umz un1 4un. 2una. 1unab un3ac un4al 
u3n2am u2n3an 2un2as un3at 1unda un4dab 1undd un4dei un4d3erf und5erha 1undf 
2undg un2did 1undn un2dor un2d3r 4unds. und3sp und3st un2d1um 1undv 1undz u3ne 
une2b une2h un2ei. un3ein unen2t un4es4 1unget 1ungew ung5h 1unglü un2g1r 
ung3ra ung3ri ung4sa un2id un3ide 1u2nif unik4 un2im uni2r 2unis un3isl u3n2it 
3u2niv 2unk un2k1a2 un2kei unks2 unk4tit unk2t3r 3unku unna2 un2n3ad un3n2e 
uno4r un2os 1unr uns2 2uns. un3se 1unsi un3sk un3sp uns4t1r 1unt un3ta unte4ri 
un3tr unt3s 2untu unvol2 unvoll3 1unw 2unz 2uo u1o2b u3of u3or. u1or3c u3ors 
uos2 u1os. uote2 u1pa u1pe2 uper1 up2fa u2pf2e u2pf1i u3pi up2pl up2pr u1pr 
up4t3a2 upt3erg upt1o up4tr u1q 2ur. u1ra u2rab u3raba ura2be u2r3a2m u2r1ana 
ur2anb u2r1ang ur2anh u2r1an5s u2rar ur3a4ren u2r3att u2r1au 2u1rä ur1än ur3b2a 
urch1 urd2 ur3di 2ure ur1eff u2rele ure4n u4r1ep ur1erh ur1erw 2urf urf3t 
ur2gri urgros4 urg3s4 uri2c ur1im ur1ini ur3ins ur1int u2rinv urk2s 1urlau 
4u1ro u3rol uro1s u1rö ur3p ur3sac ur2san ur2sau ur2ser ur4sin urst4r ur4sw 
ur3s2ze urt2 u3ru urü2 ur2za ur2zä ur2zi ur2zo ur2z1w 2us u4saf us4ann u6schent 
usch5wer u2s1ec u2s1ei u3seid u3sep use1ra u2serp u2s1ese usi3er. usi5ers. 
us3kl u4sko us3oc u3soh u2s1op us1ou us3part u2s1pas u2spat us1pe u3s2pek 
us1pic u5s4piz u2spo us2por u2spu us4sez us2sof ust3abe u1stal us3tau us2th 
ust2in us3tr u5stras us6tris u1stu u2stun u2stur us2ur u2sü 2u1ß 2u1t ut1alt 
ut3a2m u2t1ap u2t1ar u2tär u3te ut1eg ute4ge ute2n1 u2tent uter4er u4t3ersa 
ut2es ut2et u4tev u4t1ex utfi4 ut2he u2thi u2t3ho u2thu uto1 uto4ber uto3c 
ut1opf u2tops ut4or utos4 u3tö ut3rea ut3rü ut3s2a ut2s1ä ut4schl ut4schm 
ut4schö ut2spa ut3te ut5t4l utts2 utu4re utu5ru u3tü utz3eng ut2zin ut2zo 
ut2z1w 2u1u2 uufe2 u1ü2 2u1v4 u2ve. uve3rä u1w 2u1x ux2e ux2o ux3t u1ya 2u1z 
uz1we uz3z4 1üb 2übc 2übd übe2 übe3c über3 üb3l üb3r üb2s3t 2üc ü1che üch3l 
üch2s1c ücht4e ü3cken ück1er ück3eri ü4ckers ück4spe 2üd üd3a4 ü3den. üden4g 
ü3d2ens üd1o4 üd3r üd3s2 üdsa1 üd3t4 üdwes2 ü2f1a ü2f1ei üfer2 ü2f1erg üf2fl 
ü2f1i üf3l üf2to ü1g üge6leis ü2g3l ü2gn üg3s üg4st üh1a ü1he ü2h1ei ü2h1eng 
ü2h1erk ü2h1erz üh1i ühla2 ühl1ac ühl2e üh3mo üh3ne ühn2s üh3r2e ühr3ei. üh1ro 
ühr3ta üh1s ühs2p üh3t üh4th ü1hu üh1w ü1k ül1a ül2c ül4e ül2la ül2l1ei ül2lo 
ül2lö ü1lu ü2ment 2ün ü2n1a ün2da ün2dr ünd3s ünen3 ün2fa ün2f1ei ün2fli ün2fr 
ün2g3l ünn2s ün2s ün3sc ün3se ün3sp ün3str ünt2 ü1nu ün2za ü1pe ü1pi üp2pl ür1a 
ü2r1ei ür2fl ür2fr ür4g3en4g ü3r2o1 ürr2 ür2s ür3sc ür3se ür3sp ürt2h üs2a 
ü2schl üse3h üse3l üse1s üs2s1c üss2e üs2st ü2st üste3ne ü1ß 2üt ü2t1al ü2t3r 
üt2s1 üt2tr ü1v ü1z 2v1ab va1c val2s 2vang 2varb va1s v4at va2t3a4 va2tei 
va2t3h vatik2 va4t1in vati8ons. va2t3r vat3s4 va2t1u 2v1au 2v1b 2v1d 1ve2 ve3ar 
ve3b ve3c ve3d ve3g ve3h ve4i veit4 veits3 ve3la ve4l1au ve3le ve3li ve3lo 
ve3ma ve3mu ve3nal ven2c ve3ne venen4d ve3ni ve3nö ve3o ver1 ver3a ve3rad 
ve3rand ve3ras ver3b2 verd2 vere2 ve4rek verf4 verg4 ve3ri ve4rin ver3k ver3st 
vert2 ver5te ver3u ves1 2ve3sc 2ve3s2e ves3ti ve3ta vete1 ve3tr 2veü ve3v ve3x2 
2v1f4 2v1g 2v1h vi3ar vi4a3t vi2c vid3s2t vie2h3a vi2el vi2er vie4rec vie2w1 
vig2 2vii vi2l1a vi4leh vi2l1in 2v1i2m vima2 vi4na vin2s 2v1int vi3sa vise4 
vi3s2o vi2sp vis2u 2v1k 2v1l2 2v1m 2v1n 2v1ob vo3ga vo2gu 3vol voll1a vollen4 
vol6l5end vol2li 2v1op vo2r1 vor3a vor3d vor3e vor3g vo3ri vormen4 3voy vö2c 
2v1p v2r 2v3ra v3re v4ree 2v3ro 2vs vs2e v1sta v1steu v3s2z 2v3t vu2et 2vumf 
2v1v 2v1w 2v1z w2a 1waa wab2bl wa3che wach6stu wach4t4r waffe2 waffel3 1wag 
wa5ge wa2g3n wa3go 1wah wahl5ent wah4ler wah2li wai2b 1wal 2walb wal4da 2walm 
wal2ta wal2to walt4st wa3na wandels6 wang4s wa2p 1war2e ware1i war3ste wart4e 
1was wa3sa wa4scha wa3se wa3sh wass4e w2ä 1wäh 1wäl 2wäng 1wäs wäs2c wä3sche 
2w1b2 wbu2 2w1c 2w1d we2a we2ba 4webeb we2bl web3s we3cke. we5cken. we3ckes 
we2e4 weed3 we2fl 1weg we2g1a we2g3l we2g3r weg3s4 1weh we2i wei4bl 2weie weik4 
weis4s3p wei3str wei4tr wel6schl wel6schr wel2t1 wel4t3a4 wel6t5en6d wel4tr 
wen3a4 we3ni wen4k3ri we2r3a wer2bl 1werbu werd2 5werdens 1werdu werer2 wer2fl 
wer4gel we4r3io 1werk. wer2ka 1werke wer2kl wer2ku we2rö wer2s wer2ta wer6t5erm 
wer2to 1werts 1wese we2s1p we4st west1a west3ei wes2th west1o2 west3r wes4tu 
1wet wet2s wett3s 2w1ey 2w1g 2w3h wi3cka 1wid wi2e wie3l wien2e wie2st wik2 
1wil wim2ma wim4m3u win4d3e4c win2dr win2e 2wing win8n7ersc 1wi4r wi3s2e wi2sp 
1wiss wi3th 1witzl 2w1k 2w1l 2w1m 2wn wn3s 1wo1c wo2cha woche4 1woh woh2le 
1wolf wolf4s3 wol4ler wor3a wo2r3i wor2t3r wo4r3u wot2 1wöc wört2h 2w1p w2r 
w3ro 2w1s w3s2k ws2t 2w1t wti2 w2u 1wuc wul2 wul3se wun2s 4wur. wur2fa wur2s 
1wurst wus2 wus3te 1wu4t1 1wüh wül2 wün3 2w1w x1a 1xa. 2xa2b 1x2ad 1xae xa1fl 
1x2ag x3a2m x2anz 1x2as 2x1b 2xc x1ce x1ch x1cl 4x1d 1xe x1e4g 2xek xe2l xe3lei 
x1em 3x2em. x2en xen3s2 x2er. x2ere xers2 3xes 2x3eu 2x1f 2x1g 2x1h xib4 xi1c 
xich2 xide2 xi2d1em x1i2do xie3l xi3g xil1 xil2a xi2lo xi2lu xin3s2 x2is1 xis2c 
xi2se xi2so2 xis3s xis4tä xi2su x1i2tu x1j 2x1k2 2x2l2 x3lä x3le 2x1m 2x1n x1or 
4x1p xpor6ter x1q 2x1r 2x3s2 4x1t x2t1a xt2as xt1ä x2tän xtblo4 x2t1e2d x2t1ei 
x4tent x2t1er2f x2t3ev xtfi4 x2t1il2l xtra3b4 x2t3ran xt3s2 xt1u x3tur 1xu xu1a 
x1u2n xu2s 2xv 2x1w 2xy 3xy. 3xys x1z 2y1ab 1yac y1al. y1a2m yan2g y1ank y1ät 
y1b y1c2 y2chi y3chis ych3n y1d4 y1e y2ef yen4n y2ere y2es. yes2p ye2th y1f2 
y1g ygi2 ygie5 yg2l y1h yhr2 y1i4 y1j y1k2 yke3n yk3s2 y1l y2l3a2m yl4ante yl3c 
y4le. yli4n yloni1 yl3s2 y2l1u yma4t ym3p4 ympi1 y2n1o yno4d ynt2 y1nu y1of 
yom2 yon4i y1ont y1ou y1p ypa2 yp3an ype2 y2pf y3ph y2p1in ypo3 y4p3s y1r y3r2e 
y3ri yri2a yri1e y3r4o yrr2 ys2an y3s2c yse1 y3s2h y4s3l ysme3 ys2po ys1pr 
ys3t4 y1s4ty y2s1u2 y3s2z y1t2 y2te. y2tes y3to1 yu2r yure3 y1v y1w y1y y1z2 
2z3a2b zab3l za1c z1a2d za3de 2z1af za3gr 3zah 2z3a2k zale3 2z1all 2z1am 
3zambiq z1an za2na 2z3anf 3zani 2z3anl 2zarb 2zarc z1arm z1arti zar2tr 2z1arz 
z1as za1st4 2z3at3 3zaub z1au2f z3aug 3zaun zä2 2z1äc 3z2äh 2z1äm z1ärg z1ärm 
4z3b4 zbü1b zbübe3 2z3c 2z3d2 zdan2 zdä1 2z1e2ben 2zecho 2z1eck ze1e 2z1eff 
zeik4 zei3la zeile4 2z1ein zei3s4 zeist4 zei2t1a zeit5end zei4t3er zei2tr 
ze2l1a2 ze2len ze2l1er ze2l1in zell2a zel3sz zel3t2h zelu2 2z1emp 5zen. ze4n3ac 
zen3n ze2no zens2e zen4sem 3zent zent3s zen4zer z2er. ze2r3a ze2re2b 2z1ergä 
4z3ergeb z3erhal 2zerhö zerin4t zerk2 z2erl. 2zerlö z2ern zer4neb zer4n3ei 
ze2ro 2z1erq zers2 2z1ersa 4z3erste zert1a4 zer4t3ag zert4an zer6tere zer4tin 
zer6t5rau 4zerwei 2z1erz 3z2erza ze2sä ze3sc zes1e zes1i ze3sku ze2sp zessen4 
zes6s5end zes2sp zes2st ze2s3t ze3sta ze2tr 2zetts 2z1ex 2z1f4 2z1g2 zger2a 
2z1h z2hen zhir3 zi3alo zi3ar zid3r zi1erh ziers1 zi1es. zil2e 2z1imp zin2e 
zin4er 2z1inf 2z1inh zin1it zin2sa zin4ser 4zinsuf 2z1inv zi2o3 zi3op zirk2 
zirk6s zi3s2z zi1t2h 2z1j 2z3k4 2z1l2 2z1m2 zme2e 2z3n4 2z1ob 2z1of zo2gl 2z1oh 
3zol zon4ter zo2o 2zope z1or zo2ri zor4ne 2z1osz 2z3ot 2zö2f z1öl 2z3p4 2z1q 
2z3r2 4z1s2 z3sa z3sh z3sk z3sz 2z1t z2t1au z4tehe z3t2her zt3ho zt1ins z3tö 
zt3rec zt3s2 z3tü zu1 zu3a zub4 zu4ch zu3cke zud4 zudi4 zu2el zu3f4 zu2g1ar 
zu4gent zu3gl zug1un 2z1uhr zu3k 2z1um. zumen2 2zumf 2zumg 2zuml 2z1ums zun2e 
zung4 2zunt zup2fi zu3r2a z1urk 2z1url 2z1urs 2z1urt zu3s4 zu5t2 zuz2 2züb 
zür1c 2z1v zw2 z1wac 4zwah zwan2d1 z2wang z1war 2zwas 4zwäl 2zweg z2weig z1weis 
2z1wel 2z1wen 2z1wer z2werg 2z1wes 2zwet 4zwir z2wit 2z1wo z1wör z1wur 2z1wü 
4z1z z3z4a zzi1s4 z3z2o zz2ö
"""

exceptions = """
as-so-ciate as-so-ciates dec-li-na-tion oblig-a-tory phil-an-thropic present
presents project projects reci-procity re-cog-ni-zance ref-or-ma-tion
ret-ri-bu-tion ta-ble
"""

hyphenator = Hyphenator(patterns, exceptions)
hyphenate_word = hyphenator.hyphenate_word

del patterns
del exceptions

def cb_postformat(args):
    
    body = args['entry']['body']
    
    def hyphenate(match):
        if len(match.group(0)) > 10:
            return '&shy;'.join(hyphenate_word(match.group(0))) 
        else:
            return match.group(0)
    
    return re.sub('[^<:/".][a-zäöüßçáâàéèêëíñôó]+[^>/"]', hyphenate, body, flags=re.I)