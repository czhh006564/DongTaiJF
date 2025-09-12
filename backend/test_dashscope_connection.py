import dashscope
from http import HTTPStatus
import os

def test_qwen_vl_max_connection():
    """
    Tests the connection to the Dashscope qwen-vl-max model.
    """
    # The user provided the API key: sk-b98893a9f7274f64b3b3060771097aba
    # It's better to use an environment variable, but for this direct test, we'll use the key.
    api_key = "sk-b98893a9f7274f64b3b3060771097aba"
    if not api_key:
        print("ERROR: DASHSCOPE_API_KEY is not set.")
        return

    dashscope.api_key = api_key

    messages = [
        {
            "role": "user",
            "content": [
                # Using a public image URL for the test
                {"image": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg"},
                {"text": "请详细描述这张图片里的内容。"}
            ]
        }
    ]

    print("--- Starting qwen-vl-max Connection Test ---")
    print(f"Attempting to call model 'qwen-vl-max'...")

    try:
        response = dashscope.MultiModalConversation.call(
            model='qwen-vl-max',
            messages=messages
        )

        if response.status_code == HTTPStatus.OK:
            print("\n✅ SUCCESS: API call was successful!")
            print("-----------------------------------------")
            print("Model Response:")
            # The response content is also a list, get the text part
            response_text = response.output.choices[0].message.content[0]['text']
            print(response_text)
            print("-----------------------------------------")
        else:
            print(f"\n❌ FAILURE: API call failed.")
            print("-----------------------------------------")
            print(f"  Status Code: {response.status_code}")
            print(f"  Error Code: {response.code}")
            print(f"  Error Message: {response.message}")
            print("-----------------------------------------")
            print("\nTroubleshooting suggestions:")
            print("1. Verify the API key is correct and has sufficient credits.")
            print("2. Check server's network connectivity to dashscope.aliyuncs.com.")
            print("3. Ensure the 'qwen-vl-max' model is available for your account.")

    except Exception as e:
        print(f"\n❌ EXCEPTION: An unexpected error occurred during the API call.")
        print("-----------------------------------------")
        print(f"  Exception Type: {type(e).__name__}")
        print(f"  Exception Details: {e}")
        print("-----------------------------------------")

if __name__ == '__main__':
    test_qwen_vl_max_connection()