$(function() {
    
    // スクレイピングをいサービスずつ実行するためのコード
    var INTERVAL_TIME = 3000;

    (function execute_scrapings() {
        AutoScraping();
        window.setTimeout(execute_scrapings, INTERVAL_TIME);
    }());

    function AutoScraping() {
        var service_name;
        var val_signal = $('.table-wrapper').attr('name');
        var execute_check = $('#execute-check').attr('name');
        var title_name = $('#search-title').attr('name');
        
    
        if(val_signal && execute_check==='stop') {

            switch (val_signal){
                case '1':
                    service_name = 'U-NEXT';
                    break;
                case '2':
                    service_name = 'FOD';
                    break;
                case '3':
                    service_name = 'dアニメストア';
                    break;
                case '4':
                    service_name = 'Hulu';
                    break;
                case '5':
                    service_name = 'Amazon';
                    break;
                case '6':
                    service_name = 'Paravi';
                    break;
                case '7':
                    service_name = 'dTV';
                    break;
                case '8':
                    service_name = 'ABEMA';
                    break;
                case '9':
                    service_name = 'TELESA';
                    break;
                case '10':
                    service_name = 'Netflix';
                    break;
                case '11':
                    service_name = 'TSUTAYA';
                    break;
                case '12':
                    service_name = 'music.jp';
                    break;
                case '13':
                    service_name = 'クランクイン'; 
                    break;
            };

            $('#btn-wrapper').html("<button id='close-btn' class='modal-btn close-btn'>停止</button>");
            $('#execute-comment').text(`${service_name}を確認中です`);
            $('#execute-modal-wrapper').fadeIn();
            $('#execute-check').attr('name', 'run');

            var token = $('input[name="csrfToken"]').attr('value');
            $.ajaxSetup({
                beforeSend: function(xhr){
                    xhr.setRequestHeader('X-CSRFToken', token)
                }
            })
            
            $.ajax({
                type:"POST",
                url: "/execute_scraping/",
                data: {
                    'signal': val_signal,
                    'title': title_name
                },
                dataType: 'json',
                success: function(response) {
                    let getSignal = response.signal
                    let serviceNum = response.service_num
                    let result = response.result
                    let test = response.test

                    console.log('きた')
                    console.log(test)

                    switch (serviceNum){
                        case 1:
                            ReflectingResult('unext', result);
                            break;

                        case 2:
                            ReflectingResult('fod', result);
                            break;

                        case 3:
                            ReflectingResult('danime', result);
                            break;

                        case 4:
                            ReflectingResult('hulu', result);
                            break;

                        case 5:
                            ReflectingResult('amazon', result);
                            break;

                        case 6:
                            ReflectingResult('paravi', result);
                            break;

                        case 7:
                            ReflectingResult('dtv', result);
                            break;

                        case 8:
                            ReflectingResult('abema', result);
                            break;

                        case 9:
                            ReflectingResult('telesa', result);
                            break;

                        case 10:
                            ReflectingResult('netflix', result);
                            break;

                        case 11:
                            ReflectingResult('tsutaya', result);
                            break;

                        case 12:
                            ReflectingResult('music', result);
                            break;

                        case 13:
                            ReflectingResult('clunkin', result);
                            break;
                    }

                    var current_signal = $('.table-wrapper').attr('name');
                    if(current_signal) {
                        $('.table-wrapper').attr('name', getSignal);
                    }
                    $('#execute-check').attr('name', 'stop');
                    $('#execute-modal-wrapper').fadeOut();
                }
            });
        }
    };

    function ReflectingResult(service_name, result) {
        var serviceurl_list = {
            'unext': 'https://video.unext.jp/',
            'fod': 'https://fod.fujitv.co.jp/',
            'danime': 'https://anime.dmkt-sp.jp/animestore/tp_pc',
            'hulu': 'https://www.hulu.jp/',
            'amazon': 'https://www.amazon.co.jp/Prime-Video/b?node=3535604051',
            'paravi': 'https://www.paravi.jp/',
            'dtv': 'https://video.dmkt-sp.jp/?referrer=https%3A%2F%2Fwww.google.com%2F',
            'abema': 'https://abema.tv/',
            'telesa': 'https://navi.telasa.jp/',
            'netflix': 'https://www.netflix.com/jp/login?nextpage=https%3A%2F%2Fwww.netflix.com%2Fbrowse',
            'tsutaya': 'https://movie-tsutaya.tsite.jp/netdvd/dvd/top.do',
            'music': 'https://music-book.jp/video/',
            'clunkin': 'https://video.crank-in.net/',
        };

        var service_url = serviceurl_list[service_name]

        if(result==='レンタル'||result==='見放題'){
            $(`.${service_name}`).html(`<a href="${service_url}" target="_blank" rel="noopener noreferrer">${result}</a>`);
        }else{
            $(`.${service_name}`).html(result);
        };
    }


    // 停止ボタンが押された時の処理
    $('#btn-wrapper').click(function(){
        $('.table-wrapper').attr('name', '');
        $('#btn-wrapper').html('<p class="warning">停止中です。少しお待ちください</p>');
    });


   
});
