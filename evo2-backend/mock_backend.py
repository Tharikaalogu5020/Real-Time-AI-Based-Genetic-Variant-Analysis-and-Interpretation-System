import time
import random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Evo2 Mock Backend")

# Enable CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VariantRequest(BaseModel):
    variant_position: int
    alternative: str
    genome: str
    chromosome: str

@app.post("/analyze")
async def analyze_single_variant(request: VariantRequest):
    t0 = time.time()
    print(f"Received mock analysis request: {request}")
    
    # Simulate a realistic model inference delay (1.5 seconds)
    time.sleep(1.5)
    
    # Reference nucleotide (we mock it or randomly pick one)
    nucleotides = ["A", "C", "G", "T"]
    reference = random.choice([n for n in nucleotides if n != request.alternative])
    
    # Generate deterministic predictions based on the position number
    # so that the same mutation gives the same result
    seed_val = request.variant_position % 10
    
    threshold = -0.0009178519
    lof_std = 0.0015140239
    func_std = 0.0009016589
    
    if seed_val in [1, 3, 7]:
        # Pathogenic
        delta_score = threshold - random.uniform(0.0001, 0.002)
        prediction = "Likely pathogenic"
        confidence = min(1.0, abs(delta_score - threshold) / lof_std)
    else:
        # Benign
        delta_score = threshold + random.uniform(0.0001, 0.002)
        prediction = "Likely benign"
        confidence = min(1.0, abs(delta_score - threshold) / func_std)
        
    elapsed = time.time() - t0
    print(f"[TIMING] Mock Evo2 analysis took {elapsed:.4f}s")

    return {
        "position": request.variant_position,
        "reference": reference,
        "alternative": request.alternative,
        "delta_score": float(delta_score),
        "prediction": prediction,
        "classification_confidence": float(confidence)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
