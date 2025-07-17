function createParticles() {
  const bgAnimation = document.querySelector(".bg-animation");
  for (let i = 0; i < 50; i++) {
    const particle = document.createElement("div");
    particle.className = "particle";
    particle.style.left = Math.random() * 100 + "%";
    particle.style.top = Math.random() * 100 + "%";
    particle.style.width = Math.random() * 4 + 2 + "px";
    particle.style.height = particle.style.width;
    particle.style.animationDelay = Math.random() * 6 + "s";
    particle.style.animationDuration = Math.random() * 3 + 3 + "s";
    bgAnimation.appendChild(particle);
  }
}

// Initialize particles on page load
window.addEventListener("load", createParticles);

async function startAnalysis() {
  console.log("Starting analysis...");
  const btn = document.querySelector(".analyze-btn");
  const loading = document.querySelector(".loading");
  const results = document.querySelector(".results");

  // Show loading state
  btn.disabled = true;
  btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
  loading.style.display = "block";
  results.style.display = "none";

  try {
    // Perform analysis
    console.log("Fetching analyze endpoint...");
    const response = await fetch("/analyze");
    const data = await response.json();
    console.log("Received data:", data);

    if (data.error) {
      throw new Error(data.error);
    }

    // Update statistics with animation
    setTimeout(() => {
      console.log("Updating UI with results...");
      document.getElementById("modi-positive").textContent =
        data.pos_modi.toFixed(1) + "%";
      document.getElementById("modi-negative").textContent =
        data.neg_modi.toFixed(1) + "%";
      document.getElementById("rahul-positive").textContent =
        data.pos_rahul.toFixed(1) + "%";
      document.getElementById("rahul-negative").textContent =
        data.neg_rahul.toFixed(1) + "%";

      // Update prediction result
      document.getElementById("winner").textContent = data.winner;
      document.getElementById(
        "confidence"
      ).textContent = `Confidence: ${data.confidence.toFixed(1)}%`;
      document.getElementById(
        "sentiment-lead"
      ).textContent = `Sentiment Lead: ${data.sentiment_lead.toFixed(1)}%`;

      // Generate charts
      generateCharts(data);

      // Show results
      loading.style.display = "none";
      results.style.display = "block";
      console.log("Results displayed successfully");

      // Reset button
      btn.disabled = false;
      btn.innerHTML = '<i class="fas fa-chart-line"></i> Analyze Sentiment';
    }, 2000);
  } catch (error) {
    console.error("Error:", error);
    loading.style.display = "none";

    // Show error message
    const errorDiv = document.createElement("div");
    errorDiv.className = "error";
    errorDiv.textContent = "Error: " + error.message;
    document.querySelector(".container").appendChild(errorDiv);

    // Reset button
    btn.disabled = false;
    btn.innerHTML = '<i class="fas fa-chart-line"></i> Analyze Sentiment';

    // Remove error message after 5 seconds
    setTimeout(() => {
      errorDiv.remove();
    }, 5000);
  }
}

function generateCharts(data) {
  console.log("Generating charts with data:", data);
  try {
    // Bar chart with enhanced styling
    console.log("Creating bar chart...");
    Plotly.newPlot(
      "bar-chart",
      [
        {
          x: data.bar_chart.data[0].x,
          y: data.bar_chart.data[0].y,
          name: data.bar_chart.data[0].name,
          type: "bar",
          marker: {
            color: data.bar_chart.data[0].marker.color,
            line: { color: "#FFFFFF", width: 2 },
          },
          textposition: "outside",
          textfont: { size: 14, color: "#333" },
        },
        {
          x: data.bar_chart.data[1].x,
          y: data.bar_chart.data[1].y,
          name: data.bar_chart.data[1].name,
          type: "bar",
          marker: {
            color: data.bar_chart.data[1].marker.color,
            line: { color: "#FFFFFF", width: 2 },
          },
          textposition: "outside",
          textfont: { size: 14, color: "#333" },
        },
      ],
      {
        ...data.bar_chart.layout,
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        font: { family: "Poppins, sans-serif", size: 12 },
        showlegend: true,
        legend: { orientation: "h", y: 1.1 },
        margin: { l: 50, r: 50, t: 50, b: 50 },
      },
      { responsive: true, displayModeBar: false }
    );

    // Modi pie chart with enhanced styling
    console.log("Creating Modi pie chart...");
    Plotly.newPlot(
      "modi-pie",
      [
        {
          values: data.pie_data.modi.values,
          labels: data.pie_data.modi.labels,
          type: "pie",
          marker: {
            colors: data.pie_data.modi.colors,
            line: { color: "#FFFFFF", width: 2 },
          },
          textinfo: "label+percent",
          textfont: { size: 14, color: "#FFFFFF" },
          hole: 0.4,
        },
      ],
      {
        paper_bgcolor: "rgba(0,0,0,0)",
        font: { family: "Poppins, sans-serif" },
        showlegend: false,
        margin: { l: 20, r: 20, t: 20, b: 20 },
      },
      { responsive: true, displayModeBar: false }
    );

    // Rahul pie chart with enhanced styling
    console.log("Creating Rahul pie chart...");
    Plotly.newPlot(
      "rahul-pie",
      [
        {
          values: data.pie_data.rahul.values,
          labels: data.pie_data.rahul.labels,
          type: "pie",
          marker: {
            colors: data.pie_data.rahul.colors,
            line: { color: "#FFFFFF", width: 2 },
          },
          textinfo: "label+percent",
          textfont: { size: 14, color: "#FFFFFF" },
          hole: 0.4,
        },
      ],
      {
        paper_bgcolor: "rgba(0,0,0,0)",
        font: { family: "Poppins, sans-serif" },
        showlegend: false,
        margin: { l: 20, r: 20, t: 20, b: 20 },
      },
      { responsive: true, displayModeBar: false }
    );
    console.log("Charts generated successfully");
  } catch (error) {
    console.error("Error generating charts:", error);
  }
}
