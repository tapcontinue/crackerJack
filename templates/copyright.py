import isbn_hyphenate

copyright_1 = """
<head>
	<title>CoverImage</title>
	<link href="../temp.css" type="text/css" rel="stylesheet" />
</head>

<body>
	<p class="figure cover"><img src="./images/fcover.jpg" alt="fcover.jpg" /></p>
	<p class="figure img"><img src="./images/copyright.jpg" alt="copyright.jpg" /></p>
"""
	# <p class="copyright Print">Print ISBN: 978-1-5400-4197-5</p>
	# <p class="copyright ePub">ePub ISBN: 978-1-5400-8841-3</p>
	# <p class="copyright Kindle">Kindle ISBN: 978-1-5400-8842-0</p>


copyright_2 = """
	<p class="figure img"><img class="hallogo" src="./image/hallogo.png" alt="hallogo.png" /></p>
	<p class="copyright">For all works contained herein:</p>
	<p class="copyright">Unauthorized copying, arranging, adapting, recording, Internet posting, public performance,</p>
	<p class="copyright">or other distribution of music in this publication is an infringement of copyright.</p>
	<p class="copyright">Infringers are liable under the law.</p>
	<p class="copyright">Visit Hal Leonard Online at</p>
	<p class="website"><a href="http://www.halleonard.com" target="_blank">www.halleonard.com</a></p>

	<p class="copyright">Contact us:</p>
	<p class="copyright"><span class="bold">Hal Leonard</span></p>
	<p class="copyright">7777 W. Bluemound Rd.</p>
	<p class="copyright">Milwaukee, WI 53213</p>
	<p class="copyright"><a href="mailto:info@halleonard.com" target="_blank">Email: info@halleonard.com</a></p>
	<p class="copyright">In Europe, contact:</p>
	<p class="copyright"><span class="bold">Hal Leonard Europe Limited</span></p>
	<p class="copyright">42 Wigmore Street</p>
	<p class="copyright">Marylebone, London, W1U 2RN</p>
	<p class="copyright"><a href="mailto:info@halleonardeurope.com" target="_blank">Email: info@halleonardeurope.com</a></p>
	<p class="copyright">In Australia, contact:</p>
	<p class="copyright"><span class="bold">Hal Leonard Australia Pty. Ltd.</span></p>
	<p class="copyright">4 Lentara Court</p>
	<p class="copyright">Cheltenham, Victoria, 3192 Australia</p>
	<p class="copyright"><a href="mailto:ausadmin@halleonard.com.au" target="_blank">Email: ausadmin@halleonard.com.au</a></p>
"""
