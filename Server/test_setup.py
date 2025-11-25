"""
Simple test script to verify backend setup
Run this after installing dependencies
"""
import sys
from pathlib import Path

def test_imports():
    """Test if all required packages can be imported"""
    print("Testing imports...")
    
    tests = {
        'Flask': lambda: __import__('flask'),
        'Flask-CORS': lambda: __import__('flask_cors'),
        'Pillow': lambda: __import__('PIL'),
        'OpenCV': lambda: __import__('cv2'),
        'NumPy': lambda: __import__('numpy'),
        'music21': lambda: __import__('music21'),
        'oemer': lambda: __import__('oemer'),
    }
    
    results = {}
    for name, import_func in tests.items():
        try:
            import_func()
            results[name] = '✓ OK'
        except ImportError as e:
            results[name] = f'✗ FAILED: {str(e)}'
    
    return results

def test_directories():
    """Test if required directories exist"""
    print("\nTesting directories...")
    
    required_dirs = ['uploads', 'outputs', 'temp', 'models']
    results = {}
    
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists() and dir_path.is_dir():
            results[dir_name] = '✓ OK'
        else:
            results[dir_name] = '✗ MISSING'
    
    return results

def test_config():
    """Test if configuration loads correctly"""
    print("\nTesting configuration...")
    
    try:
        import config
        checks = {
            'UPLOAD_FOLDER': hasattr(config, 'UPLOAD_FOLDER'),
            'OUTPUT_FOLDER': hasattr(config, 'OUTPUT_FOLDER'),
            'MAX_FILE_SIZE': hasattr(config, 'MAX_FILE_SIZE'),
            'ALLOWED_EXTENSIONS': hasattr(config, 'ALLOWED_EXTENSIONS'),
        }
        
        results = {k: '✓ OK' if v else '✗ MISSING' for k, v in checks.items()}
        return results
    
    except Exception as e:
        return {'config.py': f'✗ FAILED: {str(e)}'}

def test_modules():
    """Test if custom modules load correctly"""
    print("\nTesting custom modules...")
    
    modules = {
        'utils': 'utils',
        'omr_processor': 'omr_processor',
        'music_processor': 'music_processor',
        'app': 'app',
    }
    
    results = {}
    for name, module_name in modules.items():
        try:
            __import__(module_name)
            results[name] = '✓ OK'
        except Exception as e:
            results[name] = f'✗ FAILED: {str(e)}'
    
    return results

def print_results(title, results):
    """Print test results in a formatted way"""
    print(f"\n{'='*50}")
    print(f"{title}")
    print('='*50)
    
    for key, value in results.items():
        status = '✓' if '✓' in value else '✗'
        print(f"{status} {key:<30} {value}")

def main():
    """Run all tests"""
    print("""
    ╔══════════════════════════════════════════╗
    ║   🎵 Backend Setup Verification          ║
    ╚══════════════════════════════════════════╝
    """)
    
    # Run tests
    import_results = test_imports()
    dir_results = test_directories()
    config_results = test_config()
    module_results = test_modules()
    
    # Print results
    print_results("Package Imports", import_results)
    print_results("Directory Structure", dir_results)
    print_results("Configuration", config_results)
    print_results("Custom Modules", module_results)
    
    # Summary
    all_results = {**import_results, **dir_results, **config_results, **module_results}
    failed = [k for k, v in all_results.items() if '✗' in v]
    
    print(f"\n{'='*50}")
    print("Summary")
    print('='*50)
    print(f"Total tests: {len(all_results)}")
    print(f"Passed: {len(all_results) - len(failed)}")
    print(f"Failed: {len(failed)}")
    
    if failed:
        print("\n⚠️  Failed tests:")
        for item in failed:
            print(f"  - {item}")
        print("\n💡 Run: pip install -r requirements.txt")
        sys.exit(1)
    else:
        print("\n✅ All tests passed! Backend is ready to run.")
        print("💡 Start the server with: python app.py")
        sys.exit(0)

if __name__ == '__main__':
    main()
