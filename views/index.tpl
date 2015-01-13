<html>
    <head>
        <title>
            Blenderfarm, XYZ Mind Inc.
        </title>
        <link rel="stylesheet" href="css?file=styles.css">
        <link rel="stylesheet" href="css?file=jquery-ui.min.css">
        <link rel="stylesheet" href="css?file=jquery-ui.structure.min.css">
        <link rel="stylesheet" href="css?file=jquery-ui.theme.min.css">
        <script src="js?file=jquery-2.1.3.min.js"></script>
        <script src="js?file=blenderfarm.js"></script>
        <script src="js?file=jquery-ui.min.js"></script>
        <script>
            $(document).ready(function () {
                $('#onprogress-content').show();
                bfobj.init_script();
                $('#onprogress-btn').click();
            });
        </script>
    </head>
    
    <body>
        <header>
            <div class="header-wrap">
            <div class="header-copy"><div>Blenderfarm Copyrights By XYZ Mind Inc.</div></div>
            <div>
                <ul class="menu-header">
                    <li id="onprogress-btn" class="menu-header-color" active="0">On Progress</li>
                    <li id="complete-btn" class="menu-header-color" active="0">Completed</li>
                    <li><input id="find-filename" type="text" placeholder="Find Folder Id"></li>
                </ul>
            </div>
            </div>
        </header>
        <main>
            <section id="onprogress-content" class="section">Data Not Ready :-)</section>
        </main>
        <footer></footer>
    </body>
</html>
