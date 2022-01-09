$(function() {
    
    // スクレイピングをいサービスずつ実行するためのコード
    var INTERVAL_TIME = 3000;

    (function execute_scrapings() {
        AutoScraping();
        window.setTimeout(execute_scrapings, INTERVAL_TIME);
    }());

    function AutoScraping() {
        let service_name;
        let val_signal = $('.table-wrapper').attr('name');
        let execute_check = $('#execute-check').attr('name');
        let title_name = $('#search-title').attr('name');
        
    
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
                    service_name = 'TSUTAYA';
                    break;
                case '11':
                    service_name = 'music.jp';
                    break;
                case '12':
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
                    let page_url = response.page_url
                    // let html_txt = response.html
                    // let plan = response.plan

                    switch (serviceNum){
                        case 1:
                            ReflectingResult('unext', page_url, result);
                            break;

                        case 2:
                            ReflectingResult('fod', page_url, result);
                            break;

                        case 3:
                            ReflectingResult('danime', page_url, result);
                            break;

                        case 4:
                            ReflectingResult('hulu', page_url, result);
                            break;

                        case 5:
                            ReflectingResult('amazon', page_url, result);
                            break;

                        case 6:
                            ReflectingResult('paravi', page_url, result);
                            break;

                        case 7:
                            ReflectingResult('dtv', page_url, result);
                            break;

                        case 8:
                            ReflectingResult('abema', page_url, result);
                            break;

                        case 9:
                            ReflectingResult('telesa', page_url, result);
                            break;

                        case 10:
                            ReflectingResult('tsutaya', page_url, result);
                            break;

                        case 11:
                            ReflectingResult('music', page_url, result);
                            break;

                        case 12:
                            ReflectingResult('clunkin', page_url, result);
                            break;
                    }

                    let current_signal = $('.table-wrapper').attr('name');
                    if(current_signal) {
                        $('.table-wrapper').attr('name', getSignal);
                    }
                    $('#execute-check').attr('name', 'stop');
                    $('#execute-modal-wrapper').fadeOut();
                    // $('#test').html(plan);
                },
                error: function() {
                    $('#alert').text("予期せぬエラーが発生しました。再度実行してください。");
                    $('.table-wrapper').attr('name', '');
                    $('#execute-check').attr('name', 'stop');
                    $('#execute-modal-wrapper').fadeOut();
                },
            });
        }
    };

    function ReflectingResult(service_name, pageurl, result) {

        if(result==='レンタル'||result==='見放題'){
            $(`.${service_name}`).html(`<a href="${pageurl}" target="_blank" rel="noopener noreferrer">${result}</a>`);
        }else{
            $(`.${service_name}`).html(result);
        };
    }


    // 停止ボタンが押された時の処理
    $('#btn-wrapper').click(function(){
        $('.table-wrapper').attr('name', '');
        $('#btn-wrapper').html('<p class="warning">停止中です。少しお待ちください</p>');
        $('#execute-check').attr('name', 'stop');
    });


   
});
