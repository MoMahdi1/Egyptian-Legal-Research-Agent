import json
import time
import requests

from app.questions import QUESTIONS

API_URL = "http://127.0.0.1:8000/research"

results = []

success = 0
failed = 0
errors = 0
total_time = 0

total = len(QUESTIONS)


# ===========================================
# Save results after every question
# ===========================================

def save_results():
    with open("evaluation_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)


# ===========================================
# Evaluation Loop
# ===========================================

for i, question in enumerate(QUESTIONS, start=1):

    print("=" * 80)
    print(f"[{i}/{total}]")
    print(question)

    start = time.time()

    try:

        response = requests.post(
            API_URL,
            json={"question": question},
            timeout=180
        )

        elapsed = round(time.time() - start, 2)

        if response.status_code == 200:

            data = response.json()

            results.append({
                "question": question,
                "execution_time": elapsed,
                "status": "success",
                "response": data
            })

            success += 1
            total_time += elapsed

            save_results()

            print(f"✅ Success ({elapsed}s)")

        else:

            results.append({
                "question": question,
                "execution_time": elapsed,
                "status": "failed",
                "status_code": response.status_code
            })

            failed += 1

            save_results()

            print(f"❌ HTTP {response.status_code}")

    except Exception as e:

        results.append({
            "question": question,
            "status": "error",
            "error": str(e)
        })

        errors += 1

        save_results()

        print(f"❌ Error: {e}")

    # Wait one second to avoid rate limits
    time.sleep(1)


# ===========================================
# Final Summary
# ===========================================

print("\n")
print("=" * 80)
print("Evaluation Finished")
print("=" * 80)

print(f"Total Questions : {total}")
print(f"Successful      : {success}")
print(f"Failed          : {failed}")
print(f"Errors          : {errors}")

if success > 0:
    print(f"Average Time    : {round(total_time / success, 2)} sec")

print("Results File    : evaluation_results.json")
print("=" * 80)