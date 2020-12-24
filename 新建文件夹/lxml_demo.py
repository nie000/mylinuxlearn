from lxml import etree

text = '''
<div>
<ul>
<li class="item-0"><a href="link1.html">first item</a></li>
<li class="item-1"><a href="link2.html">sec
ond item</a></li>
<li class="item-inactive"><a href="link3.ht
ml">third item</a></li>
<li class="item-1"><a href="link4.html">fou
rth item</a></li>
<li class="item-0"><a href="link5.html">fif
th item</a>
</ul>
</div>
'''
html = etree.HTML(text)
# result = etree.tostring(html)
# result=html.xpath('//a[@href="link1.html"]/text()')[0]  #扣取内容
result=html.xpath('//a[@href="link1.html"]/@href')[0]  #扣取内容
print(result)
