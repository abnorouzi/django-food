$(document).ready(function () {
    const datepickerDOM = $("#persianDatapicker2");
    const dateObject = datepickerDOM.persianDatepicker(
        {
        "inline": false,
        "format": "YYYY-MM-DD",
        "viewMode": "day",
        "initialValue": false,
        "minDate": false,
        "maxDate": false,
        "autoClose": true,
        "position": "auto",
        "altFormat": "lll",
        "altField": "#altfieldExample",
        "onlyTimePicker": false,
        "onlySelectOnDate": true,
        "calendarType": "persian",
        "inputDelay": 400,
        "observer": true,
        "calendar": {
            "persian": {
                "locale": "fa",
                "showHint": true,
                "leapYearMode": "algorithmic"
            },
            "gregorian": {
                "locale": "en",
                "showHint": true
            }
        },
        "navigator": {
            "enabled": true,
            "scroll": {
                "enabled": true
            },
            "text": {
                "btnNextText": "<",
                "btnPrevText": ">"
            }
        },
        "toolbox": {
            "enabled": true,
            "calendarSwitch": {
                "enabled": true,
                "format": "MMMM"
            },
            "todayButton": {
                "enabled": true,
                "text": {
                    "fa": "امروز",
                    "en": "Today"
                }
            },
            "submitButton": {
                "enabled": true,
                "text": {
                    "fa": "تایید",
                    "en": "Submit"
                }
            },
            "text": {
                "btnToday": "امروز"
            }
        },
        "timePicker": {
            "enabled": false,
            "step": 1,
            "hour": {
                "enabled": false,
                "step": null
            },
            "minute": {
                "enabled": true,
                "step": null
            },
            "second": {
                "enabled": false,
                "step": null
            },
            "meridian": {
                "enabled": false
            }
        },
        "dayPicker": {
            "enabled": true,
            "titleFormat": "YYYY MMMM"
        },
        "monthPicker": {
            "enabled": true,
            "titleFormat": "YYYY"
        },
        "yearPicker": {
            "enabled": true,
            "titleFormat": "YYYY"
        },
        "responsive": true,
//        "onSelect" : function(){
//
//            alert(`تاریخ انتخاب شده : ${date.year}/${date.month}/${date.date} ~ ${date.hour}:${date.minute}:${date.second}`);
//        }
    });

    const date = dateObject.getState().view;

});
