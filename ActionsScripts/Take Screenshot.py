from SiemplifyAction import SiemplifyAction
from SiemplifyUtils import unix_now, convert_unixtime_to_datetime, output_handler
from ScriptResult import EXECUTION_STATE_COMPLETED, EXECUTION_STATE_FAILED,EXECUTION_STATE_TIMEDOUT
import requests
import json



@output_handler
def main():
    siemplify = SiemplifyAction()

    url_list = siemplify.extract_action_param("URL(s)", print_value=True)
    html_output = siemplify.extract_action_param("HTML Format Output?", print_value=True)

    base64_list = []
    output = ""

    if ',' in url_list:
        siemplify.LOGGER.info('Detected multiple URLs to screenshot')
        obj = url_list.split(',')
        for i in obj:
            b = take_screenshot(i)
            s = {
                "url" : i,
                "screenshot" : b
            }
            base64_list.append(s)
    else:
        siemplify.LOGGER.info('Single URL detected to screenshot')
        b = take_screenshot(url_list)
        s = {
                "url" : url_list,
                "screenshot" : b
        }
        base64_list.append(s)

    siemplify.LOGGER.info(str(len(base64_list)) + ' screenshot(s) taken.')

    if html_output == True or html_output == 'true' or html_output == "True":
        for s in base64_list:
            html_image = "<h1>" + s['url'] + "</h1>"
            html_image = html_image + "<img src=\"data:image/png;base64,"+ s['screenshot'] +"\">"
            output = output + html_image + "\n"
    else:
        for s in base64_list:
            output = output + str(s) + "\n"


    status = EXECUTION_STATE_COMPLETED
    output_message = str(len(base64_list)) + " screenshot(s) taken"
    result_value = output

    siemplify.LOGGER.info("\n  status: {}\n  result_value: {}\n  output_message: {}".format(status,result_value, output_message))
    siemplify.end(output_message, result_value, status)

def take_screenshot(url):
    res = requests.get(url="http://10.22.83.205:5000/screenshot?url=" + url)
    js = res.json()
    return js['screenshot']

if __name__ == "__main__":
    main()
