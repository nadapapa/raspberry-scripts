<html>
<!-- wip -->
<head>
    <title>home security system admin</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
    <style>
      .btn {
        font-size: 50px;
      }
    </style>
</head>
<body>
  <div class="row">
    <div class="col-xs-12" style="height:30%;"></div>
  </div>
  <div class="row">
    <div class="col-xs-12">
      <form action="index.php" method="post">
          <input type="hidden" name="on" value="true"><br>
          <button type="submit" class="btn btn-primary btn-lg btn-block" value="ON">ON</button>
      </form>
      <br>
      <form action="index.php" method="post">
          <input type="hidden" name="off" value="true"><br>
          <button type="submit" class="btn btn-danger btn-lg btn-block" value="OFF">OFF</button>
      </form>
    </div>
  </div>
</body>

</html>

<?php

define('PIDFILE', '/tmp/pid');

if(!empty($_POST['on'])) {
    switchOn();
}
if(!empty($_POST['off'])) {
    switchOff();
}


function switchOn()
{
    $a = exec('sudo /home/pi/raspberry-scripts/motion.py > /tmp/log 2>&1 & echo $!');
    setPID((int)$a);

    echo('PID: '.$a);
}

function switchOff()
{
    if ($pid = getPID()) {
        exec('sudo kill -15 ' . (int)$pid);
        echo($pid . ' off');
    }
}

/**
 * @param integer $pid
 */
function setPID($pid)
{
    file_put_contents(PIDFILE, $pid);
}

/**
 * @return integer
 */
function getPID()
{
    $pid = false;

    if (file_exists(PIDFILE)) {
        $pid = fgets(fopen(PIDFILE, 'r'));
    }

    return $pid;
}
?>
