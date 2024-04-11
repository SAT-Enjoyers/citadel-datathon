DIR = cleaning/

data:
	jupyter nbconvert --to notebook --execute $(DIR)acs.ipynb
	jupyter nbconvert --to notebook --execute $(DIR)commodities.ipynb
	jupyter nbconvert --to notebook --execute $(DIR)meat_weights.ipynb
	jupyter nbconvert --to notebook --execute $(DIR)stocks.ipynb
	jupyter nbconvert --to notebook --execute $(DIR)acs_unemployment.ipynb
	jupyter nbconvert --to notebook --execute $(DIR)state_data.ipynb
	jupyter nbconvert --to notebook --execute $(DIR)nutrition_physical_activity.ipynb
	python scraping/market_cap.py
	rm $(DIR)*.nbconvert.ipynb

clean:
	rm $(DIR)*.nbconvert.ipynb
	rm udataset
