from flask import Flask, request, jsonify  
import requests  
import os  

app = Flask(__name__)

# API Key
API_KEY = "GLFFxPranto"  # নিজের API Key বসাও

@app.route('/pranto_outfit', methods=['GET'])
def get_player_info():
    uid = request.args.get('uid')
    key = request.args.get('key')

    if not uid or not key:
        return jsonify({"error": "uid and key are required"}), 400

    if key != API_KEY:
        return jsonify({"error": "Invalid API key"}), 403

    virus_urls = [
        f"https://freefire-virusteam.vercel.app/info?uid={uid}",
        f"https://freefire-virusteam.vercel.app/ind/info?uid={uid}"
    ]

    virus_data = None

    for url in virus_urls:
        response = requests.get(url)
        if response.status_code == 200:
            virus_data = response.json()
            break

    if not virus_data:
        return jsonify({"error": "Failed to fetch EquippedSkills data. Recheck uid"}), 500

    equipped_skills = virus_data.get("Equipped Items", {}).get("Equipped Skills", [])
    equipped_outfit_urls = virus_data.get("Equipped Items", {}).get("Profile", [])
    modified_outfit_ids = [url.split('id=')[-1] if 'id=' in url else url for url in equipped_outfit_urls]

    return jsonify({
        "EquippedSkills": equipped_skills,
        "ModifiedOutfitIDs": modified_outfit_ids,
        "Real Developer": "Ironmanhindigaming",
        "Credit": "PRANTO"
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  
    app.run(host='0.0.0.0', port=port, debug=True)
