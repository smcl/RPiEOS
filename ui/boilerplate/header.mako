<%!
   import os.path
%>

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>${app.AppName}</title>

    <link rel="icon" href="/static/favicon.ico" type="image/x-icon" />

    <script src="/static/jquery-1.11.3.min.js"></script>
    <script src="/static/bootstrap.min.js"></script>

    %if os.path.isfile(os.path.join(app.current_dir, "static", page + ".js")):
    <script src="/static/${page}.js"></script>
    %endif

    <link rel="stylesheet" href="/static/bootstrap.min.css">
    <link rel="stylesheet" href="/static/bootstrap-theme.min.css">
    <link rel="stylesheet" href="/static/site.css">    

    </head>

    <body>
      <div class="container container-narrow">

	    <nav class="navbar navbar navbar-static-top">
	      <a class="navbar-brand" href="/">${app.AppName}</a>
	      <ul class="nav navbar-nav">
	        <li class="nav-item">
	          <a class="nav-link" href="/about">About</a>
	        </li>
	      </ul>
	    </nav>
