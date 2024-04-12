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
	rm -f $(DIR)*.nbconvert.ipynb

eda:
	jupyter nbconvert --to notebook --execute $(EDADIR)health_clustering.ipynb
	jupyter nbconvert --to notebook --execute $(EDADIR)wealth_clustering.ipynb
	jupyter nbconvert --to notebook --execute $(EDADIR)wealth_interpolation.ipynb
	rm -f $(EDADIR)*.nbconvert.ipynb


data-old:
	jupyter nbconvert --to notebook --execute $(OLDDIR)cleaning/stocks.ipynb
	rm -f $(OLDDIR)cleaning/*.nbconvert.ipynb

clean:
	rm -f $(DIR)*.nbconvert.ipynb
	rm -rf udataset
	mkdir udataset
	mkdir udataset/acs

scrape:
	python scraping/market_cap.py
	python scraping/unemployment_rate.py