
import re

text = '<h1>快速安装指南<a class="headerlink" href="#quick-install-guide" title="永久链接至标题">¶</a></h1>'

text = """
<div class="section" id="s-install-python">\n<span id="install-python"></span><h2>安装 Python<a class="headerlink" href="#install-python" title="永久链接至标题">¶</a></h2>\n<p>作为一个 Python Web 框架，Django 需要 Python。更多细节请参见 <a class="reference internal" href="../../faq/install/#faq-python-version-support"><span class="std std-ref">我应该使用哪个版本的 Python 来配合 Django?</span></a>。Python 包含了一个名为 <a class="reference external" href="https://sqlite.org/">SQLite</a> 的轻量级数据库，所以你暂时不必自行设置一个数据库。</p>\n<p>最新版本的 Python 可以通过访问 <a class="reference external" href="https://www.python.org/downloads/">https://www.python.org/downloads/</a> 或者操作系统的包管理工具获取。</p>\n<p>你可以在你的 shell 中输入 <code class="docutils literal notranslate"><span class="pre">python</span></code> 来确定你是否安装过 Python；你看到的可能是像这样子的:</p>\n<div class="highlight-default notranslate"><div class="highlight"><pre><span></span><span class="n">Python</span> <span class="mf">3.</span><span class="n">x</span><span class="o">.</span><span class="n">y</span>\n<span class="p">[</span><span class="n">GCC</span> <span class="mf">4.</span><span class="n">x</span><span class="p">]</span> <span class="n">on</span> <span class="n">linux</span>\n<span class="n">Type</span> <span class="s2">"help"</span><span class="p">,</span> <span class="s2">"copyright"</span><span class="p">,</span> <span class="s2">"credits"</span> <span class="ow">or</span> <span class="s2">"license"</span> <span class="k">for</span> <span class="n">more</span> <span class="n">information</span><span class="o">.</span>\n<span class="o">&gt;&gt;&gt;</span>\n</pre></div>\n</div>\n</div><strong>test</strong>
"""

sub_text = re.sub(r'<h1>(.*?)</h1>', r'# \1', text)
sub_text = re.sub(r'<h2>(.*?)</h2>', r'## \1', sub_text)
sub_text = re.sub(r'<a.*?href="(.*?)".*?>(.*?)</a>', r'[\2](\1)', sub_text)
sub_text = re.sub(
    r'\.\./\.\./', r'https://docs.djangoproject.com/zh-hans/3.0/', sub_text)
sub_text = re.sub(r'\[(.*?)\]\(#.*?\)', r'\1', sub_text)
sub_text = re.sub(r'<pre>', r'```python\n', sub_text)
sub_text = re.sub(r'</pre>', r'```', sub_text)
sub_text = re.sub(r'<strong>(.*?)</strong>', r'--\1--', sub_text)
sub_text = re.sub(
    r'<div.*?>|<p>|<span.*?>|<ul.*?>|<li.*?>|</span>|</div>|</ul>|</li>|</p>', '', sub_text)
sub_text = re.sub(r'<code.*?>(.*?)</code>', r'`\1`', sub_text)
sub_text = sub_text.replace("&gt;", ">")
sub_text = sub_text.replace("&lt;", "<")
print(sub_text)
