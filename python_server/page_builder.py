


# creates an html form object that submits "program=<filename>" as parameter
def get_form(path, program_name):
	html_result = "<button type=\"submit\" name=\"program\" value=\"" + path + "\">" + program_name + "</button><br/><br/>"
	return html_result


def get_html(programs_html):
	html = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <title>Choose A Color</title>

	<!-- Twitter Bootstrap -->
	<!-- Latest compiled and minified CSS -->
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
	<!-- Optional theme -->
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap-theme.min.css">	
  </head>
  <body>
    <div class="container">
	  	<div class="starter-template">
		    <h1>leds!</h1>
		    <form action="/" method="GET">
				  <input name="hex_color" class="color" value="66ff00"/>
				  <input type="submit" value="Submit"/>
			</form>
			<form action="/" method="GET">
				brightness: (0-20) <input type="text" name="brightness">
			</form>
			<br/>
			""" + programs_html + """
		</div>
	</div> <!-- /container -->
    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <!-- Latest compiled and minified JavaScript -->
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
	<!-- color picker -->
	<script type="text/javascript" src="/jscolor/jscolor.js"></script> 
	</body>
 </html>"""
	return html

