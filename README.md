# <span style="color: #6c5ce7; border-bottom: 2px solid #6c5ce7; padding-bottom: 0.3em; display: block;">Weights.gg Unofficial API</span>

An automated image generation tool for Weights.gg, leveraging Puppeteer and an Express API to manage concurrent requests.

## <span style="color: #00b894; border-bottom: 1px solid #00b894; padding-bottom: 0.2em; display: block;">✨ Features</span>

<ul style="color: #2d3436;">
    <li style="margin-bottom: 8px;"><strong>Concurrent Image Generation:</strong> Queue system for handling multiple image requests.</li>
    <li style="margin-bottom: 8px;"><strong>API Key Authentication:</strong> Secure endpoints.</li>
    <li style="margin-bottom: 8px;"><strong>Image Status Tracking:</strong> Real-time status updates (STARTING, PENDING, COMPLETED, FAILED).</li>
    <li style="margin-bottom: 8px;"><strong>LoRA Support:</strong> Add/remove LoRA models during generation.</li>
    <li style="margin-bottom: 8px;"><strong>Preview Updates:</strong> See previews as your image generates.</li>
    <li style="margin-bottom: 8px;"><strong>Robust Error Handling:</strong> Comprehensive error management and logging.</li>
    <li style="margin-bottom: 8px;"><strong>Health Check:</strong> Monitor the bot's status with a dedicated endpoint.</li>
</ul>

## <span style="color: #00b894; border-bottom: 1px solid #00b894; padding-bottom: 0.2em; display: block;">⚠️ Warning</span>

<div style="background-color: #ffeaa7; border-left: 4px solid #fdcb6e; padding: 0.5em 1em; margin: 1em 0; color: #d63031;">
Generated images expire after 10 minutes. Download promptly!
</div>

## <span style="color: #00b894; border-bottom: 1px solid #00b894; padding-bottom: 0.2em; display: block;">🚀 Endpoints</span>

<div style="background-color: #dfe6e9; border-radius: 5px; padding: 1em; margin-bottom: 1em;">
<h3 style="color: #e17055; margin-top: 0;">Health Check</h3>
<ul>
    <li><code style="background-color: #f1f1f1; padding: 0.2em 0.4em; border-radius: 3px; font-family: monospace;">/health</code>: Checks server status.</li>
</ul>
</div>

<div style="background-color: #dfe6e9; border-radius: 5px; padding: 1em; margin-bottom: 1em;">
<h3 style="color: #e17055; margin-top: 0;">Search LoRAs</h3>
<ul>
    <li><code style="background-color: #f1f1f1; padding: 0.2em 0.4em; border-radius: 3px; font-family: monospace;">/search-loras</code>
        <ul>
            <li><span style="color: #6c5ce7; font-weight: bold;">Query Parameter</span>:
                <ul>
                    <li><code style="background-color: #f1f1f1; padding: 0.2em 0.4em; border-radius: 3px; font-family: monospace;">query</code> (required): URL-encoded search term.</li>
                </ul>
            </li>
            <li><span style="color: #00b894; font-weight: bold;">Response</span>: JSON array of LoRA objects:
                <ul>
                    <li><code style="background-color: #f1f1f1; padding: 0.2em 0.4em; border-radius: 3px; font-family: monospace;">name</code>: LoRA name.</li>
                    <li><code style="background-color: #f1f1f1; padding: 0.2em 0.4em; border-radius: 3px; font-family: monospace;">image</code>: LoRA image URL.</li>
                    <li><code style="background-color: #f1f1f1; padding: 0.2em 0.4em; border-radius: 3px; font-family: monospace;">tags</code>: Array of tags.</li>
                </ul>
            </li>
        </ul>
    </li>
</ul>
</div>

<div style="background-color: #dfe6e9; border-radius: 5px; padding: 1em; margin-bottom: 1em;">
<h3 style="color: #e17055; margin-top: 0;">Image Status</h3>
<ul>
    <li><code style="background-color: #f1f1f1; padding: 0.2em 0.4em; border-radius: 3px; font-family: monospace;">/status/:imageId</code>
        <ul>
            <li><span style="color: #6c5ce7; font-weight: bold;">Path Parameter</span>:
                <ul>
                    <li><code style="background-color: #f1f1f1; padding: 0.2em 0.4em; border-radius: 3px; font-family: monospace;">imageId</code> (required): Image ID.</li>
                </ul>
            </li>
            <li><span style="color: #00b894; font-weight: bold;">Response</span>:
                <ul>
                    <li><code style="background-color: #f1f1f1; padding: 0.2em 0.4em; border-radius: 3px; font-family: monospace;">status</code>: (STARTING, PENDING, COMPLETED, FAILED, NOT_FOUND).</li>
                    <li><code style="background-color: #f1f1f1; padding: 0.2em 0.4em; border-radius: 3px; font-family: monospace;">prompt</code>: Generation prompt.</li>
                    <li><code style="background-color: #f1f1f1; padding: 0.2em 0.4em; border-radius: 3px; font-family: monospace;">startTime</code>: Start time.</li>
                    <li><code style="background-color: #f1f1f1; padding: 0.2em 0.4em; border-radius: 3px; font-family: monospace;">lastModifiedDate</code>: Last status update.</li>
                    <li><code style="background-color: #f1f1f1; padding: 0.2em 0.4em; border-radius: 3px; font-family: monospace;">error</code>: Error message (if applicable).</li>
                </ul>
            </li>
        </ul>
    </li>
</ul>
</div>

<div style="background-color: #dfe6e9; border-radius: 5px; padding: 1em; margin-bottom: 1em;">
<h3 style="color: #e17055; margin-top: 0;">Generate Image</h3>
<ul>
    <li><code style="background-color: #f1f1f1; padding: 0.2em 0.4em; border-radius: 3px; font-family: monospace;">/generateImage</code>
        <ul>
            <li><span style="color: #6c5ce7; font-weight: bold;">Query Parameters</span>:
                <ul>
                    <li><code style="background-color: #f1f1f1; padding: 0.2em 0.4em; border-radius: 3px; font-family: monospace;">prompt</code> (required): URL-encoded prompt.</li>
                    <li><code style="background-color: #f1f1f1; padding: 0.2em 0.4em; border-radius: 3px; font-family: monospace;">loraName</code> (optional): URL-encoded LoRA name.</li>
                </ul>
            </li>
            <li><span style="color: #00b894; font-weight: bold;">Response</span>:
                <ul>
                    <li><code style="background-color: #f1f1f1; padding: 0.2em 0.4em; border-radius: 3px; font-family: monospace;">success</code>: Boolean.</li>
                    <li><code style="background-color: #f1f1f1; padding: 0.2em 0.4em; border-radius: 3px; font-family: monospace;">imageId</code>: Unique ID.</li>
                    <li><code style="background-color: #f1f1f1; padding: 0.2em 0.4em; border-radius: 3px; font-family: monospace;">imageUrl</code>: Image URL.</li>
                    <li><code style="background-color: #f1f1f1; padding: 0.2em 0.4em; border-radius: 3px; font-family: monospace;">statusUrl</code>: Status check URL.</li>
                </ul>
            </li>
        </ul>
    </li>
</ul>
</div>

<div style="background-color: #dfe6e9; border-radius: 5px; padding: 1em; margin-bottom: 1em;">
<h3 style="color: #e17055; margin-top: 0;">API Quota</h3>
<ul>
    <li><code style="background-color: #f1f1f1; padding: 0.2em 0.4em; border-radius: 3px; font-family: monospace;">/quota</code>: Retrieves API quota information.
        <ul>
            <li><span style="color: #00b894; font-weight: bold;">Response</span>: Plain text quota details.</li>
        </ul>
    </li>
</ul>
</div>
