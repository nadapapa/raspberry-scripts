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

if((bool)$_POST['on']) {
    switchOn();
}
if((bool)$_POST['off']) {
    switchOff();
}


function switchOn()
{
echo('on');
}

function switchOff()
{
echo('off');
}

/**
 * @param integer $pid
 */
function setPID($pid)
{

}

/**
 * @return integer
 */
function getPID()
{

}
?>