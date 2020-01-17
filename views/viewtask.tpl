<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="description" content="Bottle web project template" />
    <meta name="author" content="datamate" />
    <title>My UPI Project</title>
    <!-- <link rel="stylesheet" type="text/css" href="/static/bootstrap.min.css" /> -->
    <link rel="stylesheet" type="text/css" href="/static/custom.css" />
    <script type="text/javascript" src="/static/jquery.js"></script>
    <script type="text/javascript" src="/static/custom.js"></script>
    <!-- <script type="text/javascript" src="/static/bootstrap.min.js"></script> -->
  </head>

  <body>
    <div class="header">
      <button class="back" onClick="parent.location='/tasks'">
        Back
      </button>
    </div>
    <div class="">
      <h2>{{ title }}</h2>
    </div>
    <div class=""><strong>CREATED: </strong>{{ datetimee }}</div>
    <div class="">
      <strong>DESCRIPTION:</strong>
      <br />
      <p>{{ desc }}</p>
    </div>
  </body>
</html>
