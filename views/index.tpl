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
                bfobj.render_check();
            });
        </script>
    </head>
    
    <body>
        <header>
            <div class="header-wrap">
            <div class="header-copy"><div>Blenderfarm Copyrights By XYZ Mind Inc. and Oninyon</div></div>
            <div>
                <ul class="menu-header">
                    <li id="onprogress-btn" class="menu-header-color" active="0">All Queue</li>
                    <li id="complete-btn" class="menu-header-color" active="0">Progress</li>
                    <li><input id="find-filename" type="text" placeholder="Find Folder Id"></li>
                </ul>
            </div>
            </div>
        </header>
        <main>
            <section id="onprogress-content" class="section">
                <div id="onprogress-content-start"></div>
                <div id="onprogress-content-stop"></div>
            </section>
        </main>
        <footer></footer>
    </body>
</html>
