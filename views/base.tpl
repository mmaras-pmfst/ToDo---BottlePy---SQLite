<!DOCTYPE html>
<html>

<head>
	<title>Bottle Todo</title>
	<link rel="stylesheet" type="text/css" href="/static/css/main.css" />
</head>

<body>
	<div class="navigation">
		<div class="logo">
			<h1>Todo List</h1>
		</div>

		<div class="navLinks">
			<ul>
				<li><a href="/">Home</a></li>
				<li><a href="/new">New</a></li>
				<li><a href="/about">About</a></li>
			</ul>
		</div>

		<div class="burger">
			<div class="line1"></div>
			<div class="line2"></div>
			<div class="line3"></div>
		</div>
	</div>

	<div id="section" class="section">
		{{!base}}
	</div>

	<div id="footer" class="footer">
		&copy;2019 - <a href="#" id="dev"><strong>UPI</strong></a>
	</div>


</body>

</html>