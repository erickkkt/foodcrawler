import requests
import io
import os
import json
import time
from bs4 import BeautifulSoup
from bs4 import NavigableString


# Each website you crawl is a separate project (folder)
def create_project_dir(directory):
    if not os.path.exists(directory):
        print("Creating project " + directory)
        os.mkdir(directory)

def init_company_category_files():
    projectName = 'FOODY'
    create_project_dir(projectName)

def format_title(title):
    rep_chars = ['\\', '&', '!', '@', '#','$','%', '/', ':', '*', '?', '"', '<', '>', '|','.',',','(',')','{','}','[',']']

    for char in rep_chars:
        title = title.replace(char, '')
    return title

def get_Foody(url):
    source_code = requests.get(url)
    savefile = 'FOODY/foody.json'
    homeURL = 'https://www.foody.vn'
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html')
    containtDiv = soup.find('div', {'class': 'home2-panel-right ng-scope'})
    for shop in containtDiv.findAll('div', {'class':'content-item ng-scope'}):
        contentDiv = shop.find('div', {'class':'items-content'})
        reviewTag = contentDiv.find('div', {'class':'review-points green'})
        spanScore = reviewTag.fine('span')
        score = spanScore.text.replace('\r\n','').strip()
        nameDiv = contentDiv.find('div', {'class':'title fd-text-ellip'})
        linkTag = nameDiv.find('a')
        link = homeURL + linkTag.get('href')
        name = linkTag.text.replace('\r\n','').strip()
        addressDiv = nameDiv.find('div', {'class':'desc fd-text-ellip ng-binding'})
        address = addressDiv.text

        data = {'name': name, 'link': link, 'score': score, 'address': address}
        # Write JSON file
        with io.open(savefile, 'a', encoding='utf8') as outfile:
            str_ = json.dumps(data, indent=4, sort_keys=False, separators=(',', ': '), ensure_ascii=False)
            outfile.write(str_ + ',' + '\n')

def get_shop(url, fileSave):
    source_code = requests.get(url)
    # savefile = 'FOODY/foody.json'
    homeURL = 'https://www.foody.vn'
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html')
    # resultDiv = soup.find('div', {'class':'filter-results'})
    
    for shop in soup.findAll('div', {'class': 'row-item filter-result-item'}):
        contentDiv = shop.find('div', {'class': 'row-view-right'})
        reviewTag = contentDiv.find('div', {'class': 'point highlight-text'})
        score = reviewTag.text.replace('\r\n', '').strip()
        h2Div = contentDiv.find('h2')
        linkTag = h2Div.find('a')
        link = homeURL + linkTag.get('href')
        name = linkTag.text.replace('\r\n', '').strip()
        addressDiv = contentDiv.find('div', {'class': 'address'})
        address = ''
        for span in addressDiv.find('span'):
            if type(span) == NavigableString:
                continue
            if span.text is not None:
                address = address + span.text
        address = address.replace('\n', ', ')

        data = {'name': name, 'link': link, 'score': score, 'address': address}
        # Write JSON file
        with io.open(fileSave, 'a', encoding='utf8') as outfile:
            str_ = json.dumps(data, indent=4, sort_keys=False, separators=(',', ': '), ensure_ascii=False)
            outfile.write(str_ + '\n')

def get_all_comments_by_restaurant(url):
    source_code = requests.get(url)
    homeURL = 'https://www.foody.vn'
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html')
    listReviewDiv = soup.find('div', {'class': 'list-reviews'})
    comments = []
    for reviewItem in listReviewDiv.findAll('li',{'class':'review-item'}):
        name = ''
        link = ''
        score = 0
        comment = ''
        reviewUserDiv = reviewItem.find('div',{'class':'review-user'})
        reviewDesDiv = reviewItem.find('div', {'class':'review-des'})
        if reviewUserDiv is not None:
            rurowDiv = reviewUserDiv.find('div',{'class':'ru-row'})
            if rurowDiv is not None:
                linkDiv = rurowDiv.find('a')
                if linkDiv is not None:
                    link = homeURL + linkDiv.get('href')

                nameSpan = rurowDiv.find('span')
                if nameSpan is not None:
                    name = nameSpan.text.replace('\n','').strip()

        if reviewDesDiv is not None:
            reviewPointDiv = reviewDesDiv.find('div',{'class':'review-points'})
            if reviewPointDiv is not None:
                pointSpan = reviewPointDiv.find('span')
                if pointSpan is not None:
                    score = pointSpan.text.replace('\n','').strip()
            commentDiv = reviewDesDiv.find('div',{'class':'rd-des'})
            if commentDiv is not None:
                comment = commentDiv.text
        item = {'user':name, 'link':link, 'score':score, 'comment':comment}
        comments.append(item)
    return comments

def get_all_comments_by_user(url, saveFile):
    source_code = requests.get(url)
    homeURL = 'https://www.foody.vn'
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html')
    userNameDiv = None
    userNameDiv = soup.find('div',{'class':'u-name'})
    userName = ''
    if userNameDiv is not None:
        userName = userNameDiv.text

    avartar = ''
    avartarDiv = None
    avartarDiv = soup.find('div', {'class':'u-avatar'})
    if avartarDiv is not None:
        avartar = avartarDiv.find('img').get('src')
    listReviewDiv = soup.find('div', {'class':'mp-content'})
    comments = []
    for liComment in listReviewDiv.find('li',{'class':'review-item fd-clearbox'}):
        restaurant = ''
        link = ''
        restaurantNameDiv = None
        restaurantNameDiv = liComment.find('div', {'class':'res-name-row'})
        if restaurantNameDiv is not None:
            restaurantLink = restaurantNameDiv.find('a')
            link = homeURL+restaurantLink.get('href')
            restaurant = restaurantLink.text

        comment = ''
        descriptionDiv = None
        descriptionDiv = liComment.find('div',{'class':'rd-des toggle-height'})
        if descriptionDiv is not None:
            commentSpan = descriptionDiv.find('span')
            comment = commentSpan.text

        score = 0
        reviewPointDiv = None
        reviewPointDiv = liComment.find('div', {'class':'review-points'})
        if reviewPointDiv is not None:
            scoreSpan = reviewPointDiv.find('span')
            score = scoreSpan.text

        item = {'restaurant': restaurant, 'link':link, 'comment': comment, 'score': score}
        comments.append(item)

    data = {'user':userName,'avatar':avartar,'link':url, 'comments':comments}
    # Write JSON file
    with io.open(saveFile, 'a', encoding='utf8') as outfile:
        str_ = json.dumps(data, indent=4, sort_keys=False, separators=(',', ': '), ensure_ascii=False)
        outfile.write(str_ + '\n')

def get_foods_of_restaurant(url):
    foods = []
    source_code = requests.get(url)
    homeURL = 'https://www.foody.vn'
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html')
    for dishes in soup.findAll('div',{'class':'deli-box-menu-detail'}):
        h3Name = None
        h3Name = dishes.find('h3')
        name = ''
        if h3Name is not None:
            name = h3Name.text.replace('\r','').replace('\n','').strip()
        pTag = None
        pTag = dishes.find('p')
        totalOrder = 0
        if pTag is not None:
            totalSpan = pTag.find('span')
            totalOrder = totalSpan.text
        price = ''
        currentPriceP = None
        currentPriceP = dishes.find('p', {'class':'current-price'})
        if currentPriceP is not None:
            priceSpan = currentPriceP.find('span',{'class':'txt-blue font16 bold'})
            unitSpan = currentPriceP.find('span', {'class':'unit'})
            price = priceSpan.text.replace('\r','').replace('\n','').strip() + '('+unitSpan.text.replace('\r','').replace('\n','').strip() +')'

        item = {'name': name, 'price': price, 'total_orders': totalOrder}
        foods.append(item)
    return foods

def get_detail_foody(url, fileSave):
    source_code = requests.get(url)
    homeURL = 'https://www.foody.vn'
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html')
    h1Div = soup.find('h1')
    name = ''
    if h1Div is not None:
        name = h1Div.text

    categoryDiv = soup.find('div',{'class':'category'})
    categories = []
    if categoryDiv is not None:
        for category in categoryDiv.findAll('a'):
            link = homeURL + category.get('href')
            text = category.text.replace('\r','').replace('\n','').strip()
            item = {'category': text, 'link': link}
            categories.append(item)

    groupPointDiv = soup.find('div', {'class':'microsite-point-group'})
    values = []
    if groupPointDiv is not None:
        for point in groupPointDiv.findAll('div', {'class':'microsite-top-points'}):
            spanDiv = point.find('span', {'class':'avg-txt-highlight'})
            score = 0
            if spanDiv is not None:
                score = spanDiv.text.replace('\r','').replace('\n','').strip()

            labelDiv = point.find('div', {'class':'label'})
            label = ''
            if labelDiv is not None:
                label = labelDiv.text.replace('\r','').replace('\n','').strip()
            item = {'label': label, 'score':score}
            values.append(item)

    averagePointDiv = soup.find('div', {'class': 'microsite-top-points-block'})
    averageScoreDiv = None
    if averagePointDiv is not None:
        averageScoreDiv = averagePointDiv.find('div', {'class':'microsite-point-avg'})
    averageScore = 0
    if averageScoreDiv is not None:
        averageScore = averageScoreDiv.text.replace('\r','').replace('\n','').strip()

    countReviewDiv = None
    if averagePointDiv is not None:
        countReviewDiv = averagePointDiv.find('div', {'class':'microsite-review-count'})

    countReview = 0
    if countReviewDiv is not None:
        countReview = countReviewDiv.text

    summary = {'average_score':averageScore, 'total_review':countReview}

    commonAddressDiv = soup.find('div', {'class':'res-common-add'})
    address = ''
    if commonAddressDiv is not None:
        address = commonAddressDiv.text.replace('\n',' ').strip()

    commonPriceDiv = soup.find('div', {'class':'res-common-price'})

    openSpan = None
    if commonPriceDiv is not None:
        openSpan = commonPriceDiv.find('span', {'class':'itsopen'})

    openTime = ''
    if openSpan is not None:
        openTime = openSpan.get('title').replace('|','').strip()

    commonMinMaxPriceDiv = soup.find('div', {'class':'res-common-minmaxprice'})

    priceRange = ''
    if commonMinMaxPriceDiv is not None:
        priceRange = commonMinMaxPriceDiv.text.replace('\n','').strip()

    foods = []
    bookDivs = None
    bookDivs = soup.findAll('div', {'class':'microsite-table-book'})
    count = len(bookDivs)
    if bookDivs is not None and count > 0:
        bookDiv = None
        bookDiv = bookDivs[count-1]

        viewMenuDiv = None
        viewMenuDiv = bookDiv.find('div',{'class':'view-all-menu'})
        menuTitleDiv = None
        menuTitleDiv = bookDiv.find('div',{'class':'tb-title'})
        linkMenu = None
        if viewMenuDiv is not None:
            linkMenu = viewMenuDiv.find('a')
        elif menuTitleDiv is not None:
            linkMenu = menuTitleDiv.find('a')
        link = None
        if linkMenu is not None:
            link = homeURL + linkMenu.get('href')

        if link is not None:
            if 'https://www.tablenow.vn' not in link:
                foods = get_foods_of_restaurant(link)

    commentListDiv = soup.find('div', {'class':'lists list-reviews'})
    commentListUL = None
    if commentListDiv is not None:
        commentListUL = commentListDiv.find('ul', {'class':'review-list fd-clearbox'})

    userComments = []
    if commentListUL is not None:
        for commentLi in commentListUL.findAll('li', {'class':'review-item fd-clearbox foody-box-shadow'}):
            scoreCommentDiv = commentLi.find('div', {'class':'review-points green'})
            scoreSpan = None
            if scoreCommentDiv is not None:
                scoreSpan = scoreCommentDiv.find('span')

            score = 0
            if scoreSpan is not None:
                score = scoreSpan.text

            memberDiv = commentLi.find('div', {'class':'ru-row'})
            link = memberDiv.find('a')
            href = homeURL + link.get('href')
            user = link.text.replace('\n','').strip()

            commentDiv = commentLi.find('div', {'class':'rd-des'})
            commentSpan = commentDiv.find('span')
            comment = commentSpan.text.replace('\n','')

            item = {'user':user, 'link': href, 'score':score, 'comment':comment}
            userComments.append(item)


    data = {'name':name, 'link':url, 'address':address, 'open_time':openTime, 'price_range':priceRange, 'category':categories, 'values':values, 'summary':summary, 'foods':foods, 'user_comments':userComments}

    # Write JSON file
    if not os.path.isfile(fileSave):
        with io.open(fileSave, 'a', encoding='utf8') as outfile:
            str_ = json.dumps(data, indent=4, sort_keys=False, separators=(',', ': '), ensure_ascii=False)
            outfile.write(str_ + '\n')

def get_detal_all_foody_by_category(url):
    homeURL = 'https://www.foody.vn'
    projectName = 'FOODY'
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html')

    for shop in soup.findAll('div', {'class': 'row-item filter-result-item'}):
        contentDiv = shop.find('div', {'class': 'row-view-right'})
        h2Div = contentDiv.find('h2')
        linkTag = h2Div.find('a')
        link = homeURL + linkTag.get('href')
        name = linkTag.text.replace('\r\n', '').strip()
        if 'Hệ thống' in name:
            continue
        if 'Hệ Thống' in name:
            continue
        savefile = projectName + '/' + format_title(name) + '.json'
        get_detail_foody(link, savefile)

def get_detail_all_food_by_system(url):
    homeURL = 'https://www.foody.vn'
    projectName = 'FOOD-SYSTEM'
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html')
    containerDiv = None
    containerDiv = soup.find('div',{'class':'fd-padding-top fd-clearbox'})
    if containerDiv is not None:
        for shop in containerDiv.findAll('li', {'class': 'ldc-item'}):
            contentDiv = shop.find('div', {'class': 'ldc-item-h-name'})
            h2Div = contentDiv.find('h2')
            linkTag = h2Div.find('a')
            link = homeURL + linkTag.get('href')
            if '{{Model.Url}}' in link:
                continue
            name = linkTag.text.replace('\r\n', '').strip()
            savefile = projectName + '/' + format_title(name) + '.json'
            get_detail_foody(link, savefile)

def get_food_by_system():
    system = 'HETHONG'
    for filename in os.listdir(system):
        systemFile = system + '/' + filename
        try:
            with io.open(systemFile,'r', encoding='utf-8') as data_file:
                data = json.load(data_file)
                link = data['link']
                get_detail_all_food_by_system(link)
        except:
            continue


def collect_user_comments():
    foodyDir = 'UNUSERS'
    userDir = 'N-USER'
    for filename in os.listdir(foodyDir):
        foodyFile = foodyDir + '/' + filename
        userFile = userDir + '/' + filename
        with io.open(foodyFile, 'r', encoding='utf-8') as data_file:
            data = json.load(data_file)
            name = data['name']
            link = data['link']
            comments = []
            commentLink = link +'/binh-luan'
            comments = get_all_comments_by_restaurant(commentLink)
            data = {'name': name, 'link': link, 'user_comments': comments}
            # Write JSON file
            with io.open(userFile, 'a', encoding='utf8') as outfile:
                str_ = json.dumps(data, indent=4, sort_keys=False, separators=(',', ': '), ensure_ascii=False)
                outfile.write(str_ + '\n')


def get_foody_by_area():
    areas = [1,2,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,693,694,695,696,698,699]
    areas = [699]
    # 4,5- false

    url = 'https://www.foody.vn/ho-chi-minh/dia-diem?CategoryGroup=food&dtids='
    # for area in areas:
    #     success = False
    #     url = url + str(area)
    #     response = requests.get(url)
    #     while not success:
    #         time.sleep(1 / 250)
    #         if str(response) == "<Response [200]>":
    #             time.sleep(1 / 250)  # Wait Xs between API call
    #             get_detal_all_foody_by_category(url)
    #             success = True
    #         else:
    #             print(response)
    #             print(response.headers)
    #             time.sleep(3)
    #             response = requests.get(url)
    # #
    for area in areas:
        url = url + str(area)
        # fileSave = 'FOODY/' + str(area) + '.json'
        get_detal_all_foody_by_category(url)
        # get_shop(url, fileSave)

# get_detail_all_company()
#get_company_for_each_category()

#init_company_category_files()
#get_company_by_category('DEF')

#craw_data_itViec()
#area: 1,2,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,693,694,695,696,698,699
# get_shop('https://www.foody.vn/ho-chi-minh/food/dia-diem')
#get_Foody('https://www.foody.vn/#/places')
# url = 'https://www.foody.vn/ho-chi-minh/papas-chicken-beer-thu-duc'
# get_detail_foody(url, 'papachicken.json')

# urluser = 'https://www.foody.vn/thanh-vien/ngoc.anh26#/activities'
# get_all_comments_by_user(urluser, 'ngocanh.json')
# url = 'https://www.foody.vn/thuong-hieu/baoz-dimsum-restaurant?c=ho-chi-minh'
# get_detail_all_food_by_system(url)
# get_foody_by_area()
# get_food_by_system()
# urlrestaurant = 'https://www.foody.vn/ho-chi-minh/mi-cay-naga-hoa-phuong/binh-luan'
# comments = get_all_comments_by_restaurant(urlrestaurant)
# a = 1
collect_user_comments()