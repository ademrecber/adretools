from django.core.management.base import BaseCommand
from blog.models import BlogPost

class Command(BaseCommand):
    help = 'Create initial blog posts for AdSense approval'

    def handle(self, *args, **options):
        posts = [
            {
                'title': 'How to Split PDF Files Online - Complete Guide',
                'slug': 'how-to-split-pdf-files-online',
                'meta_description': 'Learn how to split PDF files online for free. Step-by-step guide to extract pages, split by range, and organize documents efficiently.',
                'content': '''
<h2>Why Split PDF Files?</h2>
<p>PDF splitting is essential for document management, sharing specific pages, reducing file sizes, and organizing content efficiently.</p>

<h3>Methods to Split PDF Files</h3>
<ul>
<li><strong>Single Page Split:</strong> Extract each page as separate file</li>
<li><strong>Range Split:</strong> Extract specific page ranges</li>
<li><strong>Interval Split:</strong> Split every N pages</li>
</ul>

<h3>Step-by-Step Guide</h3>
<ol>
<li>Upload your PDF file to AdreTools</li>
<li>Choose split method (single, range, or interval)</li>
<li>Select pages or set parameters</li>
<li>Download split files instantly</li>
</ol>

<h3>Best Practices</h3>
<p>Name your files systematically, keep original backups, and verify page content before splitting large documents.</p>

<h3>Security & Privacy</h3>
<p>All processing happens locally in your browser. Files are never uploaded to servers, ensuring complete privacy and security.</p>
'''
            },
            {
                'title': 'PDF Merge Tutorial: Combine Multiple PDFs Easily',
                'slug': 'pdf-merge-tutorial-combine-multiple-pdfs',
                'meta_description': 'Complete tutorial on merging PDF files online. Learn to combine documents, maintain quality, and organize merged PDFs effectively.',
                'content': '''
<h2>Benefits of PDF Merging</h2>
<p>Combining multiple PDFs creates organized documents, reduces file clutter, and simplifies sharing and storage.</p>

<h3>Merge Strategies</h3>
<ul>
<li><strong>Sequential Merge:</strong> Combine files in specific order</li>
<li><strong>Folder Merge:</strong> Merge entire folder contents</li>
<li><strong>Selective Merge:</strong> Choose specific pages from each file</li>
</ul>

<h3>Quality Considerations</h3>
<p>Maintain original resolution, preserve bookmarks and metadata, and optimize file size for intended use.</p>

<h3>Common Use Cases</h3>
<ul>
<li>Combining report chapters</li>
<li>Merging scanned documents</li>
<li>Creating presentation packages</li>
<li>Consolidating invoices or receipts</li>
</ul>
'''
            },
            {
                'title': 'QR Code Generator Guide: Create Custom QR Codes',
                'slug': 'qr-code-generator-guide-create-custom-codes',
                'meta_description': 'Learn to create QR codes for URLs, text, WiFi, and more. Complete guide to QR code generation, customization, and best practices.',
                'content': '''
<h2>QR Code Applications</h2>
<p>QR codes bridge physical and digital worlds, enabling instant access to websites, contact info, WiFi networks, and more.</p>

<h3>QR Code Types</h3>
<ul>
<li><strong>URL QR Codes:</strong> Direct links to websites</li>
<li><strong>Text QR Codes:</strong> Plain text messages</li>
<li><strong>WiFi QR Codes:</strong> Network connection details</li>
<li><strong>Contact QR Codes:</strong> vCard information</li>
</ul>

<h3>Design Best Practices</h3>
<p>Ensure sufficient contrast, maintain quiet zones, test readability, and choose appropriate sizes for intended use.</p>

<h3>Business Applications</h3>
<ul>
<li>Restaurant menus and ordering</li>
<li>Event registration and tickets</li>
<li>Product information and reviews</li>
<li>Marketing campaigns and promotions</li>
</ul>
'''
            },
            {
                'title': 'Image Optimization: Resize and Convert Images Online',
                'slug': 'image-optimization-resize-convert-images-online',
                'meta_description': 'Master image optimization techniques. Learn to resize, convert formats, compress images while maintaining quality for web and print.',
                'content': '''
<h2>Image Optimization Importance</h2>
<p>Optimized images improve website speed, reduce bandwidth usage, and enhance user experience across all devices.</p>

<h3>Optimization Techniques</h3>
<ul>
<li><strong>Resizing:</strong> Adjust dimensions for specific uses</li>
<li><strong>Format Conversion:</strong> Choose optimal file formats</li>
<li><strong>Compression:</strong> Reduce file size while preserving quality</li>
</ul>

<h3>Format Selection Guide</h3>
<ul>
<li><strong>JPEG:</strong> Best for photographs and complex images</li>
<li><strong>PNG:</strong> Ideal for graphics with transparency</li>
<li><strong>WebP:</strong> Modern format with superior compression</li>
</ul>

<h3>Web Performance Tips</h3>
<p>Use responsive images, implement lazy loading, and choose appropriate compression levels based on content type and viewing context.</p>
'''
            },
            {
                'title': 'Password Security: Generate Strong Passwords Online',
                'slug': 'password-security-generate-strong-passwords',
                'meta_description': 'Learn password security best practices. Generate strong passwords, understand security requirements, and protect your accounts effectively.',
                'content': '''
<h2>Password Security Fundamentals</h2>
<p>Strong passwords are your first line of defense against cyber threats. Understanding password security is crucial for digital safety.</p>

<h3>Strong Password Characteristics</h3>
<ul>
<li><strong>Length:</strong> Minimum 12 characters recommended</li>
<li><strong>Complexity:</strong> Mix of uppercase, lowercase, numbers, symbols</li>
<li><strong>Uniqueness:</strong> Different password for each account</li>
<li><strong>Unpredictability:</strong> Avoid personal information and patterns</li>
</ul>

<h3>Common Password Mistakes</h3>
<ul>
<li>Using personal information (birthdays, names)</li>
<li>Reusing passwords across multiple accounts</li>
<li>Using dictionary words or common phrases</li>
<li>Storing passwords in unsecured locations</li>
</ul>

<h3>Password Management Tips</h3>
<p>Use password managers, enable two-factor authentication, regularly update passwords, and monitor for data breaches.</p>
'''
            },
            {
                'title': 'URL Shortener Benefits: Create Short Links Effectively',
                'slug': 'url-shortener-benefits-create-short-links',
                'meta_description': 'Discover URL shortener benefits for marketing, analytics, and user experience. Learn to create effective short links and track performance.',
                'content': '''
<h2>URL Shortening Advantages</h2>
<p>Short URLs improve user experience, enable better tracking, and make sharing easier across social media and marketing campaigns.</p>

<h3>Use Cases for Short URLs</h3>
<ul>
<li><strong>Social Media:</strong> Fit character limits and look cleaner</li>
<li><strong>Print Materials:</strong> Easier to type and remember</li>
<li><strong>Email Marketing:</strong> Improve click-through rates</li>
<li><strong>QR Codes:</strong> Generate simpler, more reliable codes</li>
</ul>

<h3>Analytics and Tracking</h3>
<p>Short URLs provide valuable insights into click patterns, geographic distribution, device types, and campaign performance.</p>

<h3>Best Practices</h3>
<ul>
<li>Use descriptive custom aliases when possible</li>
<li>Test links before launching campaigns</li>
<li>Monitor link performance regularly</li>
<li>Keep backup of original URLs</li>
</ul>
'''
            },
            {
                'title': 'Color Theory for Designers: Pick Perfect Colors',
                'slug': 'color-theory-designers-pick-perfect-colors',
                'meta_description': 'Master color theory fundamentals. Learn color picking techniques, understand color psychology, and create harmonious color schemes.',
                'content': '''
<h2>Color Theory Basics</h2>
<p>Understanding color theory helps create visually appealing designs that communicate effectively and evoke desired emotional responses.</p>

<h3>Color Wheel Fundamentals</h3>
<ul>
<li><strong>Primary Colors:</strong> Red, blue, yellow - cannot be mixed</li>
<li><strong>Secondary Colors:</strong> Green, orange, purple - mixed primaries</li>
<li><strong>Tertiary Colors:</strong> Combinations of primary and secondary</li>
</ul>

<h3>Color Harmony Schemes</h3>
<ul>
<li><strong>Complementary:</strong> Opposite colors on wheel</li>
<li><strong>Analogous:</strong> Adjacent colors on wheel</li>
<li><strong>Triadic:</strong> Three evenly spaced colors</li>
<li><strong>Monochromatic:</strong> Variations of single color</li>
</ul>

<h3>Color Psychology</h3>
<p>Colors influence emotions and behavior. Red energizes, blue calms, green represents nature, and purple suggests luxury.</p>
'''
            },
            {
                'title': 'Text Analysis Tools: Analyze Content Effectively',
                'slug': 'text-analysis-tools-analyze-content-effectively',
                'meta_description': 'Comprehensive guide to text analysis tools. Learn content analysis techniques, readability metrics, and text optimization strategies.',
                'content': '''
<h2>Text Analysis Importance</h2>
<p>Text analysis helps improve content quality, readability, and SEO performance while ensuring clear communication with your audience.</p>

<h3>Key Analysis Metrics</h3>
<ul>
<li><strong>Word Count:</strong> Track content length and density</li>
<li><strong>Readability Score:</strong> Measure text complexity</li>
<li><strong>Keyword Density:</strong> Optimize for search engines</li>
<li><strong>Sentiment Analysis:</strong> Understand emotional tone</li>
</ul>

<h3>Content Optimization Strategies</h3>
<ul>
<li>Use clear, concise language</li>
<li>Vary sentence length and structure</li>
<li>Include relevant keywords naturally</li>
<li>Break up text with headings and lists</li>
</ul>

<h3>SEO Considerations</h3>
<p>Balance keyword optimization with natural language, focus on user intent, and create valuable, engaging content that serves your audience.</p>
'''
            }
        ]

        for post_data in posts:
            post, created = BlogPost.objects.get_or_create(
                slug=post_data['slug'],
                defaults=post_data
            )
            if created:
                self.stdout.write(f'Created: {post.title}')
            else:
                self.stdout.write(f'Already exists: {post.title}')