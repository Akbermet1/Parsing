import requests
from bs4 import BeautifulSoup
import csv

def get_page(url):
    source = requests.get(url)
    return source.text

def analyze_page_content(page_content):
    soup = BeautifulSoup(page_content, "lxml")
    return soup

def get_image_url(car):
    image_url = car.find("div", class_="thumb-item-carousel").find("img").get("data-src") 
    image = image_url if image_url is not None else "фото не было загружено"
    return image

def get_description(car):
    city = car.find("div", class_="item-info-wrapper").find("p", class_="city").text
    city_index = car.find("div", class_="item-info-wrapper").text.find(city)

    description = car.find("div", class_="item-info-wrapper").text
    description_formatted = description[:city_index+1].strip().replace("\n", "").replace("  ", " ")
    
    return description_formatted

def parse():
    with open("chevrolet_cars_data.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(["модель", "цена", "фото", "описание"])

        for page in range(1, 17): 
            soup = analyze_page_content(get_page(f"https://www.mashina.kg/search/chevrolet/all/?currency=2&sort_by=upped_at%20desc&time_created=all&page={page}"))
            cars_container = soup.find("div", attrs={"class": "table-view-list"})
            cars = cars_container.find_all("div", class_="list-item")
            cars = list(filter(lambda car: car.find("h2") is not None, cars))
            
            for car in cars:
                model = car.find("h2").string.strip()
                price = car.find("p").find("strong").string
                image = get_image_url(car)
                description = get_description(car)
                
                print("model:", model)
                print("price:", price)
                print("image:", image)
                print("description:", description)
                
                writer.writerow([model, price, image, description])
                
    

parse()

if __name__ == '__main__':
    parse()
    

