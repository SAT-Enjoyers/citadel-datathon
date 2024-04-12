DIR = cleaning/
EDADIR = eda/
OLDDIR = old/

all: clean scrape data eda

data:
	jupyter nbconvert --to notebook --execute $(DIR)acs_unemployment.ipynb
	jupyter nbconvert --to notebook --execute $(DIR)acs.ipynb
	jupyter nbconvert --to notebook --execute $(DIR)commodities.ipynb
	jupyter nbconvert --to notebook --execute $(DIR)health_data.ipynb
	jupyter nbconvert --to notebook --execute $(DIR)meat_weights.ipynb
	jupyter nbconvert --to notebook --execute $(DIR)meat.ipynb
	jupyter nbconvert --to notebook --execute $(DIR)national_unemployment_month.ipynb
	jupyter nbconvert --to notebook --execute $(DIR)wealth_data.ipynb
	rm $(DIR)*.nbconvert.ipynb

eda:
	jupyter nbconvert --to notebook --execute $(EDADIR)health_clustering.ipynb
	jupyter nbconvert --to notebook --execute $(EDADIR)wealth_clustering.ipynb
	jupyter nbconvert --to notebook --execute $(EDADIR)wealth_interpolation.ipynb
	rm $(EDADIR)*.nbconvert.ipynb


data-old:
	jupyter nbconvert --to notebook --execute $(OLDDIR)cleaning/stocks.ipynb
	rm $(OLDDIR)cleaing/*.nbconvert.ipynb

clean:
	rm $(DIR)*.nbconvert.ipynb
	rm udataset

scrape:
	python scraping/market_cap.py
	python scraping/unemployment_rate.py