from time import sleep

from django.http.response import JsonResponse
from django.shortcuts import redirect, render

from django.views import View

from haishincheck.utils import (
    clunkin, scraping_setting, unext, fod, danime, hulu, paravi, amazon,
    dtv, abema, telesa, tsutaya, musicjp, 
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

        # html = 'test'
        # plan ='test'

        # スクレイピングの関数実行
        driver = scraping_setting.driver_setting()

        if service_num == 1:
            result, page_url = unext.unext_scraping(driver, title)
        elif service_num == 2:
            result, page_url = fod.fod_scraping(driver, title)
        elif service_num == 3:
            result, page_url = danime.danime_scraping(driver, title)
        elif service_num == 4:
            result, page_url = hulu.hulu_scraping(driver, title)
        elif service_num == 5:
            result, page_url = amazon.amazon_scraping(driver, title)
        elif service_num == 6:
            result, page_url = paravi.paravi_scraping(driver, title)
        elif service_num == 7:
            result, page_url = dtv.dtv_scraping(driver, title)
        elif service_num == 8:
            result, page_url = abema.abema_scraping(driver, title)
        elif service_num == 9:
            result, page_url = telesa.telesa_scraping(driver, title)
        elif service_num == 10:
            result, page_url = tsutaya.tsutaya_scraping(driver, title)
        elif service_num == 11:
            result, page_url = musicjp.musicjp_scraping(driver, title)
        elif service_num == 12:
            result, page_url = clunkin.ckunkin_scraping(driver, title)


        if service_num not in range(1, 12):
            get_signal = None
            

        context = {
            'signal': get_signal,
            'service_num': service_num,
            'result': result,
            'page_url': page_url,
            # 'html': html,
            # 'plan': plan,
        }

        return JsonResponse(context)



# 404error
def page_not_found(request, exception):
    return render(request, '404.html', status=404)


# 500error
def server_error(request):
    return render(request, '500.html', status=500)

            

        

