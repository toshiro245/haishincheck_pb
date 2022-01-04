from time import sleep

from django.http.response import JsonResponse
from django.shortcuts import redirect, render

from django.views import View

from haishincheck.utils import (
    clunkin, scraping_setting, unext, fod, danime, hulu, paravi, amazon,
    dtv, abema, telesa, netflix, tsutaya, musicjp, 
)



class HomeView(View):

    def get(slef, request):
        return render(request, 'home.html')

    def post(self, request):
        title = request.POST['title']
        if not title:
            return redirect('haishin-check:home')

        context = {
            'title': title,
            'signal': 1,
        }
        return render(request, 'home.html', context)



def execute_scraping(request):
    if request.method == 'POST':
        get_signal = int(request.POST.get('signal'))
        title = request.POST.get('title')
        
        get_signal += 1
        service_num = get_signal - 1

        # スクレイピングの関数実行
        driver = scraping_setting.driver_setting()
        
        if service_num == 1:
            result = unext.unext_scraping(driver, title)
        elif service_num == 2:
            result = fod.fod_scraping(driver, title)
        elif service_num == 3:
            result = danime.danime_scraping(driver, title)
        elif service_num == 4:
            result = hulu.hulu_scraping(driver, title)
        elif service_num == 5:
            result = amazon.amazon_scraping(driver, title)
        elif service_num == 6:
            result = paravi.paravi_scraping(driver, title)
        elif service_num == 7:
            result = dtv.dtv_scraping(driver, title)
        elif service_num == 8:
            result = abema.abema_scraping(driver, title)
        elif service_num == 9:
            result = telesa.telesa_scraping(driver, title)
        elif service_num == 10:
            result = netflix.netflix_scraping(driver, title)
        elif service_num == 11:
            result = tsutaya.tsutaya_scraping(driver, title)
        elif service_num == 12:
            result = musicjp.musicjp_scraping(driver, title)
        elif service_num == 13:
            result = clunkin.ckunkin_scraping(driver, title)


        scraping_setting.driver_quit(driver)

        if service_num not in range(1, 13):
            get_signal = None
            

        context = {
            'signal': get_signal,
            'service_num': service_num,
            'result': result,
        }

        return JsonResponse(context)



# 404error
def page_not_found(request, exception):
    return render(request, '404.html', status=404)


# 500error
def server_error(request):
    return render(request, '500.html', status=500)

            

        

