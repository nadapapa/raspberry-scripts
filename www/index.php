<html>
<!-- wip -->
<head>
    <title>home security system admin</title>
</head>
<body>
    <form action="index.php" method="post">
        <input type="hidden" name="on" value="true"><br>
        <input type="submit" value="ON">
    </form>
    <br>
    <form action="index.php" method="post">
        <input type="hidden" name="off" value="true"><br>
        <input type="submit" value="OFF">
    </form>
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
