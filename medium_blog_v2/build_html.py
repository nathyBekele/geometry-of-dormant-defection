import base64
import os

def build():
    with open('probe-detectability-study/medium_blog_v2/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Fix code tag
    html = html.replace('<code>Qwen2.5-Coder-1.5B-Instruct` with seed 42.', '<code>Qwen2.5-Coder-1.5B-Instruct</code> with seed 42.')

    # Write clean index.html & medium_post_v2.html
    with open('probe-detectability-study/medium_blog_v2/index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    with open('probe-detectability-study/medium_blog_v2/medium_post_v2.html', 'w', encoding='utf-8') as f:
        f.write(html)

    # Generate standalone embedded version
    images = [
        '01_dual_policy.png',
        '02_layer_sweep.png',
        '03_inversion.png',
        '04_transfer.png',
        '05_defenses.png',
        '06_organisms.png',
        '07_layer20.png'
    ]

    embedded_html = html
    for img_name in images:
        img_path = os.path.join('probe-detectability-study/medium_blog_v2', img_name)
        if os.path.exists(img_path):
            with open(img_path, 'rb') as img_f:
                b64_data = base64.b64encode(img_f.read()).decode('utf-8')
                src_str = f'src="{img_name}"'
                b64_src = f'src="data:image/png;base64,{b64_data}"'
                embedded_html = embedded_html.replace(src_str, b64_src)

    with open('probe-detectability-study/medium_blog_v2/medium_post_v2_standalone.html', 'w', encoding='utf-8') as f:
        f.write(embedded_html)

    print('Generated index.html, medium_post_v2.html, and medium_post_v2_standalone.html')
    print('Standalone file size:', os.path.getsize('probe-detectability-study/medium_blog_v2/medium_post_v2_standalone.html'))

if __name__ == '__main__':
    build()
