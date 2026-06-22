import threading
import time
from vata_kernel.core import VATAGatewayEngine, VATAEngineException

def run_secure_agent(engine: VATAGatewayEngine):
    print(f"[*] Thread [{threading.current_thread().name}] initializing secure session...")
    with engine.execute_session_block(session_id="session_001", allowed_modules=["math"], max_calls=5) as session:
        try:
            session.intercept_module_invocation("math.sqrt")
            session.verify_and_log_call()
            print(f"[+] Thread [{threading.current_thread().name}] authorized module check passed cleanly.")
            time.sleep(2)
            session.intercept_module_invocation("math.ceil")
            session.verify_and_log_call()
        except VATAEngineException as e:
            print(f"[-] Thread [{threading.current_thread().name}] unexpected security fault: {e}")

def run_adversarial_agent(engine: VATAGatewayEngine):
    time.sleep(0.5)
    print(f"\n[!] Thread [{threading.current_thread().name}] initializing unauthenticated task loop...")
    with engine.execute_session_block(session_id="session_002", allowed_modules=["os"], max_calls=1) as session:
        try:
            print(f"[*] Thread [{threading.current_thread().name}] attempting unauthorized module invocation ('subprocess')...")
            session.intercept_module_invocation("subprocess.Popen")
        except VATAEngineException as e:
            print(f"\033[91m[+] VATA ISOLATION BOUNDARY BLOCK: {e}\033[0m")

        try:
            print(f"[*] Thread [{threading.current_thread().name}] attempting to flood tool execution calls...")
            for i in range(5):
                session.verify_and_log_call()
        except VATAEngineException as e:
            print(f"\033[91m[+] VATA RESOURCE COUNTER BLOCK: {e}\033[0m")

if __name__ == "__main__":
    shared_key = b"VATA_CORE_STANDALONE_SECRET_KEY_PROD_2026"
    kernel_engine = VATAGatewayEngine(safe_workspace_dir="./vata_safe_zone", secret_key=shared_key)
    
    t1 = threading.Thread(target=run_secure_agent, args=(kernel_engine,), name="Secure_Agent_Thread")
    t2 = threading.Thread(target=run_adversarial_agent, args=(kernel_engine,), name="Adversarial_Agent_Thread")
    
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print("\n[***] VATA INTEGRITY HARNESS COMPLETE.")
