document.write('\

<form id="searchform" action="{% url 'user-search' %}" method="get" accept-charset="utf-8">\
<button class="searchbutton" type="submit">\
<i class="fa fa-search"></i>\
</button>\
<input class="searchfield" id="searchbox" name="q" type="text" placeholder="Search">\
</form>\


');
