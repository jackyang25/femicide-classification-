# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%

##### This cell reads the news articles at the links provided by the Platform and Sayac and saves them.

import pandas as pd
femtr = pd.read_csv('/Users/nyuaduser/Dropbox/Responsiveness and Accountability/Data/Turkey_Femicide/FemicideTurkey.csv')
femtr = femtr[['Link', 'Month', 'Year', 'Name']]
Sayac = pd.read_csv('/Users/nyuaduser/Dropbox/Responsiveness and Accountability/Data/Turkey_Femicide/Turkey2All.csv')
Sayac = Sayac.rename(columns = {'ProetctionRequest': 'ProtectionRequest', 'Killer': 'Suspect', 'Place': 'Province', 'Source': 'Link', 'StatusKiller': 'Outcome'})
Sayac = Sayac[['Link', 'Date', 'Province', 'Name', 'CauseDeath', 'Suspect', 'ProtectionRequest', 'Reason', 'Image_Link', 'TxtImage', 'Outcome']]

# Extract articles from links using news-please
from newsplease import NewsPlease

# This function tells Newsplease what to extract from articles
def ExtractArt(link):
    try:
        article = NewsPlease.from_url(link, timeout = 20)
        date = article.date_publish
        title = article.title
        description = article.description
        maintext = article.maintext
        lang = article.language
        output = (date, title, description, maintext, lang)
        return output
    except:
        return tuple()

# For some reason I need to run this function on a link before it will actually work. Without this line the code just runs forever.
ExtractArt(femtr.Link[0])

# Extracting links from the Platform's dataset
Text = []
N = len(femtr)

# This module gives a progress bar
import tqdm
# This module parallelizes the extraction
from pathos.multiprocessing import ProcessingPool as Pool

# Even with parallelizing this takes a few minutes
with Pool(8) as p:
    Text = list(tqdm.tqdm(p.imap(ExtractArt, femtr.Link), total=N))      

articles = pd.DataFrame(Text, columns =['Article_Date', 'Title', 'Description', 'Text', 'lang'])     
#Paste together the two data sets:
articles = pd.concat([femtr, articles],axis=1,sort=False)

# articles.to_csv('~/Dropbox/Responsiveness and Accountability/Data/Turkey_Femicide/femtrArticles.csv', encoding='utf-8-sig', index=False)

# Extracting links from the Sayac dataset
Text = []
N = len(Sayac)

with Pool(8) as p:
    Text = list(tqdm.tqdm(p.imap(ExtractArt, Sayac.Link), total=N))      

articles = pd.DataFrame(Text, columns =['Article_Date', 'Title', 'Description', 'Text', 'lang'])     
#Paste together the two data sets:
articles = pd.concat([Sayac, articles],axis=1,sort=False)

# articles.to_csv('~/Dropbox/Responsiveness and Accountability/Data/Turkey_Femicide/SayacArticles.csv', encoding='utf-8-sig', index=False)

# %%
##### This cell extracts province information from the news articles and fixes provinces.

# After looking for a lot of different methods I decided that manually entering the list of provinces in Turkey is the most straightforward way
provinces_tr = ["Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Aksaray", "Amasya", "Ankara", "Antalya", "Ardahan", "Artvin", "Aydın", "Balıkesir", "Bartın", "Batman", "Bayburt", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Düzce", "Edirne", "Elazığ", "Erzincan", "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkâri", "Hatay", "Iğdır", "Isparta", "İstanbul", "İzmir", "Kahramanmaraş", "Karabük", "Karaman", "Kars", "Kastamonu", "Kayseri", "Kilis", "Kırıkkale", "Kırklareli", "Kırşehir", "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Mardin", "Mersin", "Muğla", "Muş", "Nevşehir", "Niğde", "Ordu", "Osmaniye", "Rize", "Sakarya", "Samsun", "Şanlıurfa", "Siirt", "Sinop", "Sivas", "Şırnak", "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Uşak", "Van", "Yalova", "Yozgat", "Zonguldak"]
locations_tr = ["Başkent", "Afyon", "İzmit", "Adapazarı", "DÜZCE", "Dersim", "Çorlu", "Bodrum", "Ayvalık", "Alanya", "Fethiye", "Çiğli", "Akyazı", "Mazıdağı", "Antakya"]
locations_tr.append(provinces_tr)

import re
import numpy as np
# This function searches for provinces names provided in the list above in the text of the scraped news articles
def search_province_names(data, names, index):
        try:
            return re.search(names, str(data.Link[index].replace('/', ' ').replace('-', ' ')) + str(data.Title[index]) + str(data.Text[index]) + str(data.Description[index]))[0]
        except (TypeError, AttributeError) as e:
            return None

# ### Matching provinces from the Platform articles
# FemicideTurkey = pd.read_csv('/Users/nyuaduser/Dropbox/Responsiveness and Accountability/Data/Turkey_Femicide/femtrArticles.csv')

# # Creating a list of length len(FemicideTurkey) * len(provinces_tr)
# province_matches = [search_province_names(FemicideTurkey, i, j) for i in provinces_tr for j in range(len(FemicideTurkey))]
# # Reshaping the above list to a dataframe of nrows = len(FemicideTurkey) and ncols = len(provinces_tr)
# Provinces = pd.DataFrame(np.transpose(np.array(province_matches).reshape(len(provinces_tr), len(FemicideTurkey))), columns = provinces_tr)
# # Turning the above dataframe back to a list where each row is name(s) of province(s) mentioned in the article
# Provinces_Combined = Provinces.apply(lambda x: None if x.isnull().all() else ', '.join(x.dropna()), axis=1)
# FemicideTurkey['Province'] = Provinces_Combined

# # FemicideTurkey.to_csv('~/Dropbox/Responsiveness and Accountability/Data/Turkey_Femicide/femtr_with_Articles.csv', encoding='utf-8-sig', index=False)


# ### Matching provinces from the Sayac articles
# Sayac = pd.read_csv('/Users/nyuaduser/Dropbox/Responsiveness and Accountability/Data/Turkey_Femicide/SayacArticles.csv')

# # Creating a list of length len(Sayac) * len(provinces_tr)
# province_matches = [search_province_names(Sayac, i, j) for i in provinces_tr for j in range(len(Sayac))]
# # Reshaping the above list to a dataframe of nrows = len(Sayac) and ncols = len(provinces_tr)
# Provinces = pd.DataFrame(np.transpose(np.array(province_matches).reshape(len(provinces_tr), len(Sayac))), columns = provinces_tr)
# # Turning the above dataframe back to a list where each row is name(s) of province(s) mentioned in the article
# Provinces_Combined = Provinces.apply(lambda x: None if x.isnull().all() else ', '.join(x.dropna()), axis=1)
# Sayac['Province2'] = Provinces_Combined

# # Sayac.to_csv('~/Dropbox/Responsiveness and Accountability/Data/Turkey_Femicide/Sayac_with_Articles.csv', encoding='utf-8-sig', index=False)


# %%

import pandas as pd
# Loading data collected from different sources and cleaning them.
FemicideTurkey = pd.read_csv('/Users/nyuaduser/Dropbox/Responsiveness and Accountability/Data/Turkey_Femicide/old/femtr_with_Articles.csv')
Ermin1 = pd.read_csv('/Users/nyuaduser/Dropbox/Responsiveness and Accountability/Data/Turkey_Femicide/old/serkanermin4.csv')
Ermin2 = pd.read_csv('/Users/nyuaduser/Dropbox/Responsiveness and Accountability/Data/Turkey_Femicide/old/serkanerminnn.csv')
Sayac = pd.read_csv('/Users/nyuaduser/Dropbox/Responsiveness and Accountability/Data/Turkey_Femicide/old/Sayac_with_Articles.csv')
Ermin2['Name'] = Ermin2['name and age'].str.split(',').str[0]
Ermin2['Name'] = Ermin2['Name'].str.split('(\d+)').str[0]
Ermin2 = Ermin2.drop(Ermin2[Ermin2['Name'].str.contains('http')].index)

# Listing Turkish characters and their English equivalents
translationTable = str.maketrans("âğĞıİöÖüÜşŞçÇ", "agGiIoOuUsScC")

# Listing different names of provinces as well as regions within provinces so everything will be aggregated at the province level.
othernames = {'Baskent': 'Ankara', 'Afyon': 'Afyonkarahisar', 'Izmit': 'Kocaeli', 'Adapazari': 'Sakarya', 'Dersim' :'Tunceli', 'Corlu': 'Tekirdag', 'Ayvalik': 'Balikesir', 'Akyazi': 'Sakarya', 'Mazidagi': 'Mardin', 'Antakya': 'Hatay', 'Urfa': 'Sanliurfa'}
istanbul_ilce = ["Adalar", "Arnavutköy", "Ataşehir", "Avcılar", "Bağcılar", "Bahçelievler", "Bakırköy", "Başakşehir", "Bayrampaşa", "Beşiktaş", "Beykoz", "Beylikdüzü", "Beyoğlu", "Büyükçekmece", "Çatalca", "Çekmeköy", "Esenler", "Esenyurt", "Eyüp", "Fatih", "Gaziosmanpaşa", "Güngören", "Kadıköy", "Kağıthane", "Kartal", "Küçükçekmece", "Maltepe", "Pendik", "Sancaktepe", "Sarıyer", "Silivri", "Sultanbeyli", "Sultangazi", "Şile", "Şişli", "Tuzla", "Ümraniye", "Üsküdar", "Zeytinburnu"]
istanbul_ilce = [i.translate(translationTable) for i in istanbul_ilce]
ankara_ilce = ["Akyurt", "Altındağ", "Ayaş", "Balâ", "Beypazarı", "Çamlıdere", "Çankaya", "Çubuk", "Elmadağ", "Etimesgut", "Evren", "Gölbaşı", "Güdül", "Haymana", "Kahramankazan", "Kalecik", "Keçiören", "Kızılcahamam", "Mamak", "Nallıhan", "Polatlı", "Pursaklar", "Sincan", "Şereflikoçhisar", "Yenimahalle"]
ankara_ilce = [i.translate(translationTable) for i in ankara_ilce]
izmir_ilce = ['Aliağa', 'Balçova', 'Bayındır', 'Bayraklı', 'Bergama', 'Beydağ', 'Bornova', 'Buca', 'Çeşme', 'Çiğli', 'Dikili', 'Foça', 'Gaziemir', 'Güzelbahçe', 'Karabağlar', 'Karaburun', 'Karşıyaka', 'Kemalpaşa', 'Kınık', 'Kiraz', 'Konak', 'Menderes', 'Menemen', 'Narlıdere', 'Ödemiş', 'Seferihisar', 'Selçuk', 'Tire', 'Torbalı', 'Urla']
izmir_ilce = [i.translate(translationTable) for i in izmir_ilce]
antalya_ilce = ['Akseki', 'Aksu', 'Alanya', 'Demre', 'Döşemealtı', 'Elmalı', 'Finike', 'Gazipaşa', 'Gündoğmuş', 'İbradı', 'Kaş', 'Kemer', 'Kepez', 'Konyaaltı', 'Korkuteli', 'Kumluca', 'Manavgat', 'Muratpaşa', 'Serik']
antalya_ilce = [i.translate(translationTable) for i in antalya_ilce]
mugla_ilce = ['Bodrum', 'Dalaman', 'Datça', 'Fethiye', 'Kavaklıdere', 'Köyceğiz', 'Marmaris', 'Milas', 'Menteşe', 'Ortaca', 'Seydikemer', 'Ula', 'Yatağan']
mugla_ilce = [i.translate(translationTable) for i in mugla_ilce]

othernames.update(dict.fromkeys(istanbul_ilce, 'Istanbul'))
othernames.update(dict.fromkeys(ankara_ilce, 'Ankara'))
othernames.update(dict.fromkeys(izmir_ilce, 'Izmir'))
othernames.update(dict.fromkeys(antalya_ilce, 'Antalya'))
othernames.update(dict.fromkeys(mugla_ilce, 'Mugla'))

# Getting rid of Turkish characters, standardizing separators, and making it all title case
FemicideTurkey.Province = [i.translate(translationTable).title() if type(i) is str else "" for i in FemicideTurkey.Province]
Ermin1.Province = [i.replace(' ', '').replace(',', ', ').replace('/', ', ').translate(translationTable).title() if type(i) is str else "" for i in Ermin1.Province]
Ermin2.province = [i.replace(' ', '').replace(',', ', ').replace('/', ', ').translate(translationTable).title() if type(i) is str else "" for i in Ermin2.province]
Sayac.Province = [i.translate(translationTable).title() if type(i) is str else "" for i in Sayac.Province]
Sayac.Province2 = [i.translate(translationTable).title() if type(i) is str else "" for i in Sayac.Province2]

# Replacing non-standard names and region names to province names, but keeping place names as they are if they're not in the dictionary.
FemicideTurkey.Province = [', '.join(set(othernames.get(i, i) for i in j.split(', '))) for j in FemicideTurkey.Province]
Ermin1.Province = [', '.join(set(othernames.get(i, i) for i in j.split(', '))) for j in Ermin1.Province]
Ermin2.province = [', '.join(set(othernames.get(i, i) for i in j.split(', '))) for j in Ermin2.province]
Sayac.Province = [', '.join(set(othernames.get(i, i) for i in j.split(', '))) for j in Sayac.Province]
Sayac.Province2 = [', '.join(set(othernames.get(i, i) for i in j.split(', '))) for j in Sayac.Province2]

provinces_tr_ASCII = [i.translate(translationTable) for i in provinces_tr]

def reduce_to_provinces(dataset, varname):
    temp = []
    for i in range(len(dataset)):
        try:
            if set(dataset[varname][i].split(', ')).isdisjoint(set(provinces_tr_ASCII)):
                temp.append('')
            else:
                temp.append(', '.join(set(dataset[varname][i].split(', ')) & set(provinces_tr_ASCII)))
        except AttributeError:
            temp.append('')
    return temp

Ermin2.reset_index(drop = True, inplace = True)

FemicideTurkey.Province = reduce_to_provinces(FemicideTurkey, 'Province')
Ermin1.Province = reduce_to_provinces(Ermin1, 'Province')
Ermin2['Province'] = reduce_to_provinces(Ermin2, 'province')
Sayac.Province = reduce_to_provinces(Sayac, 'Province')
Sayac.Province2 = reduce_to_provinces(Sayac, 'Province2')

Ermin1['Province'][Ermin1.Name == "Gülşah Aktürk"] = 'Konya'
Ermin1['Province'][Ermin1.Name == "Fatma Gürdal"] = 'Sakarya'
Ermin2['Province'][Ermin2.Name == "Fatma Gürdal"] = 'Sakarya'

# If Sayac.Province and Sayac.Province2 exist, and they have a non-zero intersection, take their intersection. If their intersection is empty, manually check. If only one exists, take that. 
for i in range(len(Sayac)):
    if len(Sayac.Province[i]) > 0 & len(Sayac.Province2[i]) > 0:
        if len(list(set(Sayac.Province[i]) & set(Sayac.Province2[i]))) > 0:
            Sayac.Province[i] = list(set(Sayac.Province[i]) > 0 & set(Sayac.Province2[i]))
        else:
            Sayac.Province[i] = Sayac.Province[i] + ', ' + Sayac.Province2[i]
    elif len(Sayac.Province[i]) > 0:
        Sayac.Province[i] = Sayac.Province[i]
    elif len(Sayac.Province2[i]) > 0:
        Sayac.Province[i] = Sayac.Province2[i]

Ermin2 = Ermin2[['Name', 'date', 'suspect', 'reason', 'Province']] 
Sayac.drop(columns = ['Province2', 'lang'], inplace = True)

############################################################################################################


# Merging these into one dataframe with all names, months, and years, and more information if we have them.
femtr = FemicideTurkey.merge(Ermin1, "outer", on = ["Name", "Province"])
femtr = femtr.merge(Ermin2, "outer", on = ["Name", "Province"])
femtr = femtr.merge(Sayac, "outer", on = ["Name", "Province"])
femtr['Name'] = femtr['Name'].str.title().str.rstrip('.').str.lstrip(' ').str.rstrip(' ').str.strip('\n')
femtr = femtr.drop(femtr[femtr['Name'].str.len() < 6].index)
femtr.dropna(subset = ['Name'], inplace = True)
femtr.drop(femtr[femtr.Name == 'İsmi Bilinmiyor'].index, inplace = True)
femtr.drop(femtr[femtr.Name == 'Tespit Edilemeyen'].index, inplace = True)
femtr.drop(femtr[femtr.Name == 'Bilinmiyor'].index, inplace = True)
femtr.drop(femtr[femtr.Name == 'İsimsiz'].index, inplace = True)
femtr.drop(columns = ['Unnamed: 0', 'lang'], inplace = True)

for i in femtr.Name[femtr.duplicated(subset='Name', keep=False)]:
    temp = femtr[femtr.Name == i]
    try:
        if len(temp) > 1:
            for j in range(len(temp) - 1):
                for k in range(j + 1, len(temp)):
                    if (len(temp.Province.iloc[j]) > 0) & (len(temp.Province.iloc[k]) > 0):
                        temp_inter = list(set(temp.iloc[j].Province.split(', ')) & set(temp.iloc[k].Province.split(', ')))
                        if len(temp_inter) > 0:
                            femtr.loc[(femtr.Name == i) & (femtr['Province'].str.contains(temp_inter[0])), 'Province'] = temp_inter[0]
                    elif len(temp.Province.iloc[j]) > 0:
                        femtr.loc[(femtr.Name == i) & (femtr['Province'] == ''), 'Province'] = temp.Province.iloc[j]
                    elif len(temp.Province.iloc[k]) > 0:
                        femtr.loc[(femtr.Name == i) & (femtr['Province'] == ''), 'Province'] = temp.Province.iloc[k]    
    except AttributeError:
        pass

# The following are manually fixed or dropped
femtr.Name[femtr.Name == "Ayşegül Ç"] = "Ayşegül Çelik"
femtr.Name[femtr.Name == "Aynur C"] = "Aynur Canıtez"
femtr.Name[femtr.Name == "A. M. M. A. O"] = "A.M.M.A.O"
femtr.Name[(femtr.Name == "Bahar Topal") & (femtr.Province == "Bingol")] = "Zeynep Topal"
femtr.Name[(femtr.Name == "Fatma A") & (femtr.Province == "Osmaniye")] = "Fatma Altun"
femtr.Name[(femtr.Name == "Fatma A") & (femtr.Province == "Sakarya")] = "Fatma Acar"
femtr.Name[(femtr.Name == "Fatma A") & (femtr.Province == "Zonguldak")] = "Fatma Akyol"
femtr.Name[femtr.Name == "Meral U"] = "Meral Uzda"
femtr.Name[(femtr.Name == "Meryem K") & (femtr.Province == "")] = "Meryem Kaplan"
femtr.Name[femtr.Name == "Turna Gül Ç"] = "Turna Gül Çuntar"
femtr.Name[(femtr.Name == "Dilek A") & (femtr.Province == "")] = "Dilek Alır"
femtr.Name[(femtr.Name == "Dilek A") & (femtr.Province == "Zonguldak")] = "Dilek Akyol"
femtr.Name[(femtr.Name == "Dilek A") & (femtr.Province == "Ankara")] = "Dilek Akbulut"
femtr.Name[(femtr.Name == "Dilek Ö") & (femtr.Province == "Kocaeli")] = "Dilek Ören"
femtr.Name[(femtr.Name == "Dilek Ö") & (femtr.Province == "Van")] = "Dilek Özister"
femtr.Name[(femtr.Name == "Esme El H") | (femtr.Name == "Esme El F")] = "Esme El Hüseyin"
femtr.Name[(femtr.Name == "Fatma D") & (femtr.Province == "Kocaeli")] = "Fatma Durmaz"
femtr.Name[(femtr.Name == "Fatma D") & (femtr.Province == "Gaziantep")] = "Fatma Demir"
femtr.Name[(femtr.Name == "Fatma D") & (femtr.Province == "Eskisehir")] = "Fatma Hanlı"

femtr.Province[femtr.Name == "Sedef Şen"] = "Canakkale"
femtr.Province[(femtr.Name == "Ayşe Şahin") & (femtr.Province == "")] = "Denizli"
femtr.Province[(femtr.Name == "Fatma Demir") & (femtr.Province == "")] = "Elazig"
femtr.Province[(femtr.Name == "Hatice Şahin") & (femtr.Province == "")] = "Afyonkarahisar"
femtr.Province[(femtr.Name == "Hatice Şahin") & (femtr.Province == "Corum, Kocaeli, Samsun")] = "Samsun"
femtr.Province[(femtr.Name == "Hülya Aydın") & (femtr.Province == "Adana, Istanbul, Izmir, Aydin")] = "Izmir"
femtr.Province[(femtr.Name == "Hülya Aydın") & (femtr.Province == "Tokat, Aydin")] = "Tokat"
femtr.Province[femtr.Name == "Emine Orki"] = "Adiyaman"
femtr.Province[femtr.Name == "Nevin Nilitaş"] = "Manisa"
femtr.Province[femtr.Name == "Meral Uzda"] = "Hatay"
femtr.Province[(femtr.Name == "Ayşe Güneş") & ((femtr.Province == "Bingol, Kocaeli, Zonguldak"))] = "Zonguldak"
femtr.Province[femtr.Name == "Suna Özbey"] = "Izmir"
femtr.Province[(femtr.Name == "Fatma Yılmaz") & (femtr.Province == "")] = "Kutahya"
femtr.Province[(femtr.Name == "Aysel Şahin") & (femtr.Province == "")] = "Afyonkarahisar"
femtr.Province[femtr.Name == "Arzu Dikal"] = "Tokat"
femtr.Province[femtr.Name == "Aysun B"] = "Elazig"
femtr.Province[femtr.Name == "Aysun Yeşil"] = "Usak"
femtr.Province[femtr.Name == "Ayşe Hündür"] = "Samsun"
femtr.Province[(femtr.Name == "Ayşe Şahin") & (femtr.Province == "")] = "Denizli"
femtr.Province[femtr.Name == "Ayşegül Aslan"] = "Mugla"
femtr.Province[(femtr.Name == "Bedriye Kargı") & (femtr.Province == "")] = "Trabzon"
femtr.Province[femtr.Name == "Belma Çınar"] = "Mardin"
femtr.Province[(femtr.Name == "Şeyma Şahin") & (femtr.Province == "")] = "Ankara"
femtr.Province[femtr.Name == "Meryem Kaplan"] = "Kirikkale"
femtr.Province[femtr.Name == "Turna Gül Çuntar"] = "Kayseri"
femtr.Province[(femtr.Name == "Hatice Öztürk") & (femtr.Province == "Ankara, Zonguldak")] = "Samsun"
femtr.Province[(femtr.Name == "Songül Yılmaz") & (femtr.Province == "")] = "Samsun"
femtr.Province[(femtr.Name == "Özlem Yıldırım") & (femtr.Province == "Istanbul, Bursa")] = "Bursa"
femtr.Province[femtr.Name == "Nermin Yumuşak"] = "Tekirdag"
femtr.Province[femtr.Name == "Esme El Hüseyin"] = "Konya"
femtr.Province[(femtr.Name == "Gizem Bulut") & (femtr.Province == "")] = "Eskisehir"
femtr.Province[femtr.Name == "Seher Çetintaş"] = "Istanbul"
femtr.Province[(femtr.Name == "Emine Şahin") & (femtr.Province == "Gaziantep")] = "Sanliurfa"
femtr.Province[(femtr.Name == "Fatma Demir") & (femtr.Province == "Gaziantep, Aydin")] = "Gaziantep"
femtr.Province[(femtr.Province == 'Gaziantep, Sanliurfa') & (femtr.Name.str.contains("Şahin"))] = "Sanliurfa"
femtr.Province[(femtr.Province == 'Gaziantep, Sanliurfa') & (femtr.Name.str.contains("Tülay"))] = "Gaziantep"

femtr.Outcome[(femtr.Name == "Hülya Aydın") & (femtr.Province == "Adana, Istanbul, Izmir, Aydin")] = "Tutuklu"
femtr.Outcome[(femtr.Name == "Hatice Öztürk") & (femtr.Province == "Samsun")] = "Intihar"

istanbul_names = ["Bahar Saluğu", "Ayşegül Çelik", "Ayşegül Aktürk", "Ayten Adıgüzel Deligözoğlu", "Aleyna Can", "Arzu Özkan", "Ayşe Solmaz"]
antalya_names = ["Anna Safaryan", "Asiye Güzel"]
kocaeli_names = ["Ayşe Dayıoğlu", "Bahar Akbaş"] 
bursa_names = ["Çimen Çaymaklar", "Aynur Canıtez"]
ankara_names = ["Emine Yanıkoğlu", "Muazzez Kınay"]

femtr.Province[femtr.Name.isin(istanbul_names)] = "Istanbul"
femtr.Province[femtr.Name.isin(antalya_names)] = "Antalya"
femtr.Province[femtr.Name.isin(kocaeli_names)] = "Kocaeli"
femtr.Province[femtr.Name.isin(bursa_names)] = "Bursa"
femtr.Province[femtr.Name.isin(ankara_names)] = "Ankara"

femtr.drop(femtr[(femtr.Name == 'Aysel Şahin') & (femtr.Province == "Kars")].index, inplace = True)
femtr.drop(femtr[femtr.Name == "A.M.M.A.O"].index, inplace = True)
femtr.drop(femtr[(femtr.Name == 'Dilek Ö') & (femtr.Province == "")].index, inplace = True)


femtr = femtr.groupby(['Name', 'Province']).first().reset_index()

# femtr.to_csv('~/Dropbox/Responsiveness and Accountability/Data/Turkey_Femicide/femtr_clean_names.csv', encoding='utf-8-sig', index=True)


# %%
## This cell cleans and standardizes dates from different sources for scraping.

import pandas as pd
femtr = pd.read_csv('~/Dropbox/Responsiveness and Accountability/Data/Turkey_Femicide/femtr_clean_names.csv')


# Reconciling dates from different sources. The Platform gets priority, if that's not available I choose the earliest from others. If no date is available I set it to 2010 January 1.
import locale
from datetime import datetime

locale.setlocale(locale.LC_ALL, 'tr_TR.utf-8')
DATE_FORMATS = ['%d %B %Y', '%d/%m/%Y', '%d.%m.%Y', '%d %B %y', '%d/%m/%y', '%d.%m.%y']
# 'Year' and 'Month' are from the Platform, and 'Date' and 'date' are from Serkan Ermin. date0 collects all months and years from the Platform and sets the date to the first of that month. 
# date0 = femtr['Year'].astype(str) + " " + femtr['Month'].str.lower().replace("hazi̇ran", "haziran") + " " + "1"
date0 = []
date1 = []
date2 = []
date5 = []

# This loops writes the dates from Serkan Ermin to vectors. The first part collects dates from a standard format, and just gives the first of the month. The second part deals with multiple formats: tries each of them. Both assign January 1 2021 if they can't find anything.
for i in range(len(femtr)):
    try:
        date0.append(datetime.strptime(femtr['Year'].astype(str) + " " + femtr['Month'].str.lower().replace("hazi̇ran", "haziran") + " " + "1"), '%Y.0 %B %d')
    except (ValueError, TypeError):
        date0.append(datetime(2021, 1, 1, 0, 0))    
    try:
        date2.append(datetime(datetime.strptime(femtr['date'][i], '%m/%d/%y').year, datetime.strptime(femtr['date'][i], '%m/%d/%y').month, 1))
    except (ValueError, TypeError):
        date2.append(datetime(2021, 1, 1, 0, 0))
    flag1 = 0
    flag2 = 0
    for format in DATE_FORMATS:   
        try:
            date1.append(datetime(datetime.strptime(femtr['Date_x'][i], format).year, datetime.strptime(femtr['Date_x'][i], format).month, 1))
            flag1 = 1
        except (ValueError, TypeError):
            pass
        try:
            date5.append(datetime(datetime.strptime(femtr['Date_y'][i], format).year, datetime.strptime(femtr['Date_y'][i], format).month, 1))
            flag2 = 1
        except (ValueError, TypeError):
            pass
    if flag1 == 0:
        date1.append(datetime(2021, 1, 1, 0, 0))
    if flag2 == 0:
        date5.append(datetime(2021, 1, 1, 0, 0))        

# Takes the earliest of the two Serkan Ermin dates, ignores those for which we have data from the Platform, and appends the others to the date vector. Finally, changes January 1 2021 to January 1 2010 and appends the vector to the dataframe. Resulting column is date from the Platform if we have it, the earlier of Serkan Ermin dates if we have data from him but not the Platform, and January 1 2010 if we don't have any data.  
date3 = [min(l0, l1, l2, l5) for l0, l1, l2, l5 in zip(date0, date1, date2, date5)]      
date4 = [i if i != datetime(2021, 1, 1, 0, 0) else datetime(2010, 1, 1, 0, 0) for i in date3]
femtr['Date'] = date4

femtr.to_csv('~/Dropbox/Responsiveness and Accountability/Data/Turkey_Femicide/femtr.csv', encoding='utf-8-sig', index=True)

#%%

##### This cell scrapes Twitter with names collected from different sources

import os
import re
import json
import pandas as pd    
import snscrape
from datetime import datetime

femtr = pd.read_csv('~/Dropbox/Responsiveness and Accountability/Data/Turkey_Femicide/femtr.csv')

input_raw = 'snscrape --jsonl twitter-search'
#path for saving .json files 
path = r'/Users/kk2352/Dropbox/RA Data/TurkeyFemicide2'

for query in range(len(femtr)):
    # Creating a new folder for each femicide. 
    newpath = path + '/' + re.sub('[^A-Za-z0-9]+', '',  femtr['Name'][query])
    if not os.path.exists(newpath):
        os.makedirs(newpath) 
    os.chdir(newpath)
    # Start date is the first of the month of the killing, end date is end of 2020. 
    StartDate = datetime.strptime(femtr['Date'][query][:10], "%Y-%m-%d").date()
    EndDate = datetime.strptime('2020-12-31', "%Y-%m-%d").date()
    # File name removes all punctuation and spaces.
    FileName = re.sub('[^A-Za-z0-9]+', '',  femtr.Name[query]) + '_' + str(femtr.index[query]).zfill(4) + '_' + str(femtr.Province[query])
    # If we only have the initial of the last name, append "cinayet" to the search
    if len(femtr['Name'][query].split()[-1]) == 1:
        search =  '"' + femtr.Name[query] + '" ' + 'cinayet' + ' since:' + str(StartDate) + ' until:' + str(EndDate)
    elif femtr.Name[femtr.duplicated(subset='Name', keep=False)].isin([femtr.Name[query]]).any():
        search =  '"' + femtr.Name[query] + '" ' + femtr.Province[query] + ' since:' + str(StartDate) + ' until:' + str(EndDate)
    else:
        search =  '"' + femtr.Name[query] + '"' + ' since:' + str(StartDate) + ' until:' + str(EndDate)
    search2 =  '"#' + femtr.Name[query].replace(' ','') + '"' + ' since:' + str(StartDate) + ' until:' + str(EndDate)
    # Runs the command via the console and writes the output into a .json file in the specified file name.
    input_crawl = input_raw + ' ' + "'" + search + "'" + ' > ' +FileName +'.json'
    input_crawl2 = input_raw + ' ' + "'" + search2 + "'" + ' > ' +FileName +'_hashtag' + '.json'
    print(input_crawl)
    os.system(input_crawl)
    os.system(input_crawl2)

# %%

##### This cell reads tweets from json and writing them on separate csv files for each victim 

import glob
import os
import pandas as pd
from os import listdir

dirname = globals()['_dh'][0]

# inputDir = '~/Dropbox/RA Data/TurkeyFemicide2'
inputDir = os.path.abspath(os.path.join(dirname, '..', '..', 'RA Data', 'TurkeyFemicide2'))

Names = listdir(inputDir)
Tweets = []

j = 0
for name in Names:
    print(name)
    j+= 1
    print(j)
    NewDir = inputDir + '/' + name
    if os.path.isdir(NewDir):
        os.chdir(NewDir)    
        Files = glob.glob('*.json')
        m = []
        if len(Files)>0:
            location = Files[0].split('_')[2]
            name = Files[0].split('_')[0]
            for file in Files: 
                try:
                    data = pd.read_json(file,lines=True)
                except:
                    pass
                if len(m) == 0:
                    m = data
                else:
                    m = pd.concat([m,data])
            m['Name'] = name
            m['Location'] = location
        if len(m) > 0 :    
            outputDir = os.path.abspath(os.path.join(dirname, '..', '..', 'RA Data', 'TweetsInCSV2'))
            FileName = outputDir + '/' + name + '.csv'
            m.to_csv(FileName)

#%%

##### This cell cleans and lemmatizes each tweet
### WARNING: doesn't work on Jupyter notebook, I run it as a script on terminal instead

# import numpy as np
import glob
import os
import pandas as pd
from os import listdir
import advertools as adv
import re
import stanza 

stop_words = adv.stopwords['turkish']
nlp = stanza.Pipeline(lang='tr', processors='tokenize,pos,lemma',tokenize_pretokenized=True)

from pathlib import Path

inputDir = Path("/Users/kk2352/Dropbox/RA Data/TweetsInCSV2")
# dirname = globals()['_dh'][0]

# inputDir = os.path.abspath(os.path.join(dirname, '..', '..', 'RA Data', 'TweetsInCSV2'))

os.chdir(inputDir)
Files = glob.glob('*.csv')

start = 'location'
end = 'protected'

def cleanTweets(tweet):
    #remove punctuation and numbers
    tweet = re.sub('\n', ' ',tweet)
    tweet = re.sub(r"http\S+", '', tweet)
    tweet = re.sub(r"#\S+", '', tweet)
    tweet = re.sub(r"(?:\@|https?\://)\S+", "", tweet)
    tweet = re.sub(r'[^\w\s]', ' ', tweet)  
    #remove stop words:
    tweet_clean = [w for w in tweet.split() if not w in stop_words]
    tweet_clean = ' '.join(tweet_clean)
    #lemmatization: 
    doc = nlp(tweet_clean)
    lemmas = [word.lemma for sent in doc.sentences for word in sent.words]
    lemmas = [w for w in lemmas if not w in stop_words]
    tweet_clean = ' '.join(lemmas)
    return tweet_clean


def ProcessCSV(file):
    data = pd.read_csv(file,lineterminator='\n', dtype = {'retweetedTweet': 'unicode', 'quotedTweet': 'unicode'})
    data = data.drop(['Unnamed: 0'],axis=1)
    data = data.drop_duplicates().reset_index()
    data = data.drop(['index'],axis=1)
    dataTR = data[data['lang']=='tr'].reset_index()
    dataTR = dataTR.drop(['index'],axis=1)
    dataTR['Hashtags'] = [re.findall(r"#(\w+)", tweet) for tweet in dataTR['content']]
    dataTR['location'] = [(x.split(start))[1].split(end)[0] for x in dataTR['user']]
    dataTR['location'] = [re.sub(r'[^\w\s]', '', x) for x in dataTR['location']]
    dataTR['cleanTweet'] = [cleanTweets(text) for text in dataTR['content']]
    dataTR =  dataTR[dataTR['cleanTweet'].notna()]
    return dataTR

j = 0
k = 0
df = []

for file in Files:
    print(j)
    try:
        dta = ProcessCSV(file)
        if len(df)==0:
            df = dta
        else:
            df = pd.concat([df,dta],ignore_index=True)
    except IndexError:
        k += 1
        print(pd.read_csv(file,lineterminator='\n')['Location'][0] + " caused an IndexError")
    j += 1

dfFinal = df[['date','url','user','replyCount', 'retweetCount', 'likeCount','quoteCount',
                    'retweetedTweet', 'quotedTweet', 'Name', 'Location', 'Hashtags', 'cleanTweet','location']]


# dfFinal.to_csv(os.path.abspath(os.path.join(dirname, '..', '..', 'RA Data', 'CleanTweets3.csv')), header = False)

dfFinal.to_csv(Path("/Users/kk2352/Dropbox/RA Data/CleanTweets3.csv"))

# %%

#### This cell reads the news articles at the links we collected from Google News.

import pandas as pd
# newslinks = pd.read_csv('/Users/nyuaduser/Dropbox/Responsiveness and Accountability/Algorithms/GoogleNewsTR/GoogleNewsLinks.csv')
newslinks = pd.read_csv("/Users/nyuaduser/Dropbox/Responsiveness and Accountability/Algorithms/Google2/GoogleNewsLinks2.csv")
# Extract articles from links using news-please
from newsplease import NewsPlease

# This function tells Newsplease what to extract from articles
def ExtractArt(link):
    try:
        article = NewsPlease.from_url(link, timeout = 20)
        date = article.date_publish
        title = article.title
        description = article.description
        maintext = article.maintext
        lang = article.language
        output = (date, title, description, maintext, lang)
        return output
    except:
        return tuple()

# Extracting links
Text = []
N = len(newslinks)

# For some reason I need to run this function on a link before it will actually work. Without this line the code just runs forever.
ExtractArt(newslinks.links[0])

# This module gives a progress bar
import tqdm
# This module parallelizes the extraction
from pathos.multiprocessing import ProcessingPool as Pool

# Even with parallelizing this takes a few minutes
with Pool(8) as p:
    Text = list(tqdm.tqdm(p.imap(ExtractArt, newslinks.links), total=N))

articles = pd.DataFrame(Text, columns =['Article_Date', 'Title', 'Description', 'Text', 'lang'])     
# Paste together the two data sets:
articles = pd.concat([newslinks, articles],axis=1,sort=False)

articles.to_csv('~/Dropbox/Responsiveness and Accountability/Data/newsArticles3.csv', encoding='utf-8-sig', index=False)

#%%
## Discard pile

# import itertools
# # Ok I'm pretty proud of this. First, subset the data to duplicated names and loop over them.
# for i in femtr.Name[femtr.duplicated(subset='Name', keep=False)]:
#     temp = femtr[femtr.Name == i]
#     # Next, loop over subsets that share the same name, starting with pairs, then triplets etc.
#     for L in range(2, len(temp.Province)+1):
#         for subset in itertools.combinations(temp.Province, L):
#             try:
#                 # Finally, find intersections of provinces in these subsets if any exist and replace the rows in the dataset. If intersection is empty, pass.
#                 temp_inter = list(set.intersection(*map(set, [i.split(', ') for i in subset])))[0]
#                 femtr.Province[(femtr.Name == i) & (femtr['Province'].str.contains(temp_inter))] = temp_inter
#             except IndexError:
#                 pass
# # Above is extremely slow though.

# %%
