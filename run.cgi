#!/usr/local/bin/php74
<!DOCTYPE html>
<head>
    <meta charset="UTF-8">
</head>
<body>
    <?php
        $out = shell_exec('sh ./run.sh');
        echo $out ;
    ?>
</body>
</html>