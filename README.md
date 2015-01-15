pypharaoh
=========

Pyramid Utilities

Classes

[Scaffolds](#scaffolds)


## <a name="scaffolds">Scaffolds</a>

### SRBB Platform Stack
This is our basic application stack. It includes the following primary modules.

#### Primary Platform
* [Pyramid](http://www.pylonsproject.org/) Web Server Framework
* [SQLAlchemy](http://www.sqlalchemy.org/) Database abstraction.
* [Require.js](http://requirejs.org/) Modularized Javascript for the browser.
* [Backbone.js](http://backbonejs.org/) Model/View Javascript Framework
* [Bootstrap](http://getbootstrap.com/) UI/UX Framework

#### Included Services
* [Pyramid AuthTKT](http://docs.pylonsproject.org/docs/pyramid/en/latest/api/authentication.html) for Authentication
* [Pyramid ACL](http://docs.pylonsproject.org/docs/pyramid/en/latest/api/authorization.html) for Authorization
* [uWSGI](https://uwsgi-docs.readthedocs.org/en/latest/) for Production Web Server
* [Formencode](http://www.formencode.org/en/latest/) for data validation.
* [pyTZ](http://pytz.sourceforge.net/) for timezone handling.


#### Possible structure

``api``, ``admin`` and ``web`` modules may not reference each other as we do not want them coupled with each other.

```
+==	[package]\
	+== api\
	+== admin\
		+== assets\
		+== templates\
	+==	web\
		+==	assets\
		+== templates\
	+== models\
	+== validators\
	+== auth\
	+==	static\
```


#### Platform Directory Structure

```
+== [package]\		Main web application directory.
|	+==	static\ 		Front End static assets, templates, and framework implementations.
|	|	+== css\			Cascading StyleSheets
|	|	|	+== lib\			3rd Party Stylesheets (Bootstrap)
|	|	|	+--	style.css 		Site main style sheet
|	|	+==	img\			Images
|	|	+==	js\				Javascript
|	|	|	+==	lib\			3rd Party Javascript (Require, Backbone, etc.)
|	|	|	+--	models.js		Backbone.js Models/Collections
|	|	|	+--	templates.js	
|	|	|	+-- views.js
|	|	+==	tmpl\  			Underscore Rendered Templates
|	+== models\
|		+--	__init__.py
|	+==	templates\
|	+== views\
|		+--	__init__.py
+==	core\			Library shared by the Webapp, Admin panel and RESTful API.
|	+== scripts\		Database initialization and console scripts.  
|	+==	models\			Data models.
|	|	+--	__init__.py
|	|	+--	auth.py			Authentication Data models.
|	+==	validators\		Data validators.
|		+--	__init__.py
|	+-- __init__.py
|	+--	auth.py			Authentication functions.
+--	CHANGES.txt  	CHANGES file.
+--	MANIFEST.in  	MANIFEST file.
+--	README.md  		README markdown file.
+--	dev.ini  		Development application configuration.
+--	stage.ini  		Staging application configuration.
+--	prod.ini  		Production application configuration.
+--	setup.py		Application installation script.
```

### SRBB Stack (Extended)
This provides the same stack as SRBB but separates the RESTful API and the front end framework.