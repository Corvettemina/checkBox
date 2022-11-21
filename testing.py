import os

#paths = ""PowerPoints/doxologies/stmarkdoxologies.pptx","
#newPath = paths.split("/")
#tempPath = ('/').join(newPath[:(len(newPath)-1)])

# print(tempPath)
dictionary = {'standardPsalm150': 6, 'Psalm150': 7, 'Fraction to the Father for Advent and the Nativity': 3}


finishedList = ["PowerPoints/BackBone/Vespers.pptx",
"PowerPoints/BackBone/PrayerOfThanksgiving.pptx",
"PowerPoints/Nativity Fast/KihakVespersVerseOfCymbals.pptx",
"PowerPoints/BackBone/LitanyofTheDeparted.pptx",
"PowerPoints/BackBone/GraciouslyAccordOLord.pptx",
"PowerPoints/BackBone/HolyHolyHoly-InroToDoxologies.pptx",
"powerpoints/nativity fast/doxologies/01kihakvirgindoxology.pptx",
"powerpoints/nativity fast/doxologies/02khiakgabrildoxology.pptx",
"powerpoints/nativity fast/doxologies/03johnthebaptistdoxology.pptx",
"PowerPoints/BackBone/DoxolgyConclusion.pptx",
"PowerPoints/BackBone/IntroToTheCreed.pptx",
"PowerPoints/BackBone/Creed.pptx",
"PowerPoints/BackBone/oGodHaveMercyUponUS.pptx",
"PowerPoints/BackBone/litanyofthegospel.pptx",
"Readings/2022/12December/17-2022-dec-18/Vespers Gospel.pptx",
"PowerPoints/Nativity Fast/WeSendYouGreetingsGospelResonse.pptx",
"PowerPoints/BackBone/absolutionToTheSon.pptx",
"PowerPoints/Nativity Fast/ConclusionNativityFast.pptx",
"PowerPoints/BackBone/Conclusion.pptx",
"PowerPoints/BackBone/Matins.pptx",
"PowerPoints/BackBone/PrayerOfThanksgiving.pptx",
"PowerPoints/Nativity Fast/KihakVespersVerseOfCymbals.pptx",
"PowerPoints/BackBone/matinsLitanies.pptx",
"PowerPoints/BackBone/LetUsPraiseWithTheAngels.pptx",
"PowerPoints/BackBone/HolyHolyHoly-InroToDoxologies.pptx",
"powerpoints/nativity fast/doxologies/01kihakvirgindoxology.pptx",
"powerpoints/nativity fast/doxologies/02khiakgabrildoxology.pptx",
"powerpoints/nativity fast/doxologies/03johnthebaptistdoxology.pptx",
"PowerPoints/BackBone/DoxolgyConclusion.pptx",
"PowerPoints/BackBone/IntroToTheCreed.pptx"
"PowerPoints/BackBone/Creed.pptx",
"PowerPoints/BackBone/oGodHaveMercyUponUS.pptx",
"PowerPoints/BackBone/litanyofthegospel.pptx",
"Readings/2022/12December/17-2022-dec-18/Matins Gospel.pptx",
"PowerPoints/Nativity Fast/WeSendYouGreetingsGospelResonse.pptx",
"PowerPoints/BackBone/absolutionToTheSon.pptx",
"PowerPoints/Nativity Fast/ConclusionNativityFast.pptx",
"PowerPoints/BackBone/Conclusion.pptx",
"PowerPoints/Agpeya/AnnualTransition.pptx",
"PowerPoints/Agpeya/Third Hour Intro.pptx",
"powerpoints/agpeya/3rd hour psalms/psalm 19.pptx",
"PowerPoints/Agpeya/6th Hour Intro.pptx",
"powerpoints/agpeya/6th hour psalms/psalm 56.pptx",
"PowerPoints/Agpeya/Gospelstoday.pptx",
"PowerPoints/BackBone/IntroToTheCreed.pptx",
"PowerPoints/BackBone/Creed.pptx",
"PowerPoints/BackBone/OfferingSelection.pptx",
"PowerPoints/BackBone/AlleluiaThisIsTheDay.pptx",
"PowerPoints/BackBone/OfferingPrayerOfThanksgiving.pptx",
"PowerPoints/BackBone/thisCenser.pptx",
"PowerPoints/Nativity Fast/Hiten.pptx",
"Readings/2022/12December/17-2022-dec-18/Pauline.pptx",
"Readings/2022/12December/17-2022-dec-18/Catholic.pptx",
"PowerPoints/Nativity Fast/PraxisResponse.pptx",
"Readings/2022/12December/17-2022-dec-18/Acts.pptx",
"PowerPoints/Annual/StandardAgios.pptx",
"PowerPoints/BackBone/AnotherLitanyOftheGospel.pptx",
"Readings/2022/12December/17-2022-dec-18/LiturgyPsalm.pptx",
"Readings/2022/12December/17-2022-dec-18/LiturgyGospel.pptx",
"PowerPoints/Agpeya/AnnualTransition.pptx",
"PowerPoints/Nativity Fast/WeSendYouGreetingsGospelResonse.pptx",
"PowerPoints/BackBone/inTheWisdomOfGod.pptx",
"PowerPoints/Liturgy/Creed.pptx",
"powerpoints/liturgy/reconciliation prayers/o god the great the eternal.pptx",
"PowerPoints/Liturgy/Anaphora - Basiltoday.pptx",
"PowerPoints/Liturgy/TheCherubim.pptx",
"PowerPoints/Liturgy/Agios - Basil.pptx",
"PowerPoints/Liturgy/Institution - Basil.pptx",
"PowerPoints/Liturgy/Seven Litanies.pptx",
"PowerPoints/Liturgy/Litany of the Seeds.pptx",
"PowerPoints/Liturgy/ConclustionofTheSeason.pptx",
"PowerPoints/Liturgy/Healing to the Sick.pptx",
"PowerPoints/Liturgy/Obliations Liturgy.pptx",
"PowerPoints/Liturgy/Commemoration - Basil.pptx",
"PowerPoints/Liturgy/Post Commemoration - Gregorian.pptx",
"PowerPoints/Liturgy/Preface - Basil.pptx",
"PowerPoints/Fraction Index/Fraction to the Father for Advent and the Nativity.pptx",
"PowerPoints/Liturgy/Post Fraction.pptx",
"PowerPoints/Annual/standardPsalm150.pptx",
"PowerPoints/BackBone/communionMenuTemplate.pptx",
"PowerPoints/nativity fast/communion hymns/god eternal 3 young men.pptx",
"PowerPoints/nativity fast/communion hymns/my heart and my tounge.pptx",
"PowerPoints/nativity fast/communion hymns/kiahk doxologies.pptx",
"PowerPoints/nativity fast/communion hymns/a dove appeared at zacharias house.pptx",
"PowerPoints/nativity fast/communion hymns/amen alleluia.pptx",
"PowerPoints/BackBone/finalConclusion1.pptx",
"PowerPoints/Nativity Fast/ConclusionNativityFast.pptx",
"PowerPoints/BackBone/Conclusion.pptx",
"PowerPoints/Agpeya/AnnualTransition.pptx"]

from mergepptxaspose import merge
#merge(finishedList)

test = ["1","2","1","4","5"]
i = 0
print((test.index("1",1)))

'''
for path, subdirs, files in os.walk(""PowerPoints/"):
    for name in files:
        #print(os.path.join(path, name).lower())
        if (os.path.join(path, name).lower() == paths.lower()):
            print(os.path.join(path, name))
            break
'''
