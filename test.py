from scrapy.selector import Selector

test = '<center> <div style="max-width:860px"> <img src="http://image1.coupangcdn.com/image/vendor_inventory/c265/01c3a545cefa64552ee7bdf7c97a9c3ad3bd5ff9c155077601ed7600a6ff.jpg"> <img src="http://image1.coupangcdn.com/image/vendor_inventory/081b/1c32008a10cee73ba99e02bfe7679aad96e3b17f305b2e173164554f8115.jpg"> <img src="http://image1.coupangcdn.com/image/vendor_inventory/b2ac/1406e15e0ddad664cf5528a47f299b77f88df202e1e81bdafc8597b201e2.jpg"> <img> <img src="http://image1.coupangcdn.com/image/vendor_inventory/3c30/dedc4106d278f97d597200ac88fcefd0e0e1778350857fed7033384cfd13.jpg"> <img src="http://image1.coupangcdn.com/image/vendor_inventory/8337/48612727533b5bc0234842f614aa841b3de9d31e2d0b08125280bf940446.jpg"> <img src="http://image1.coupangcdn.com/image/vendor_inventory/e414/4df39c4f22bd1218462e1fd8d326ec1123fdf0ba7e7aaae6337e148313ea.jpg"> <img src="http://image1.coupangcdn.com/image/vendor_inventory/f74d/847585128bb321c278daf5bef37df0a42630088a04881bacb1453de394c2.jpg"> <img src="http://image1.coupangcdn.com/image/vendor_inventory/815e/a0d577999e5a8333c5e3112549428a1cc6e9aab90501a257b85aeee085db.jpg"> <img src="http://image1.coupangcdn.com/image/vendor_inventory/d875/877af448559be0486e6756300624b06aed7963268e4c759c1f053a3437a2.jpg"> <img src="http://image1.coupangcdn.com/image/vendor_inventory/980d/14d5824443d2343e40632f4a85b9be772d88d86169c4473bdc5782391e7a.jpg"> <img src="http://image1.coupangcdn.com/image/vendor_inventory/ea8c/4215ed5975314ef596f298d2f943430c68b5209fe820290c296c6f3c97b0.jpg"> <img src="http://image1.coupangcdn.com/image/vendor_inventory/0111/2afc7a305ccd5ddeb2f82fe6a194bdca617fd9e98817dc8810b2925ebccc.jpg"> <img src="http://image1.coupangcdn.com/image/vendor_inventory/e8be/3ffeaa5da6252e33ed70a0084d2c3b039397cc5a4970f91ce6604c664975.jpg"> <img src="http://image1.coupangcdn.com/image/vendor_inventory/832e/0286402ac4d41053723cf0777c78704ae688522a4827559fcc2ed38b09f0.jpg"> <img src="http://image1.coupangcdn.com/image/vendor_inventory/832e/0286402ac4d41053723cf0777c78704ae688522a4827559fcc2ed38b09f0.jpg"> <img> </div> </center>'


s = Selector(text=test)

res = s.xpath('//img/@src').extract()

print(res)
