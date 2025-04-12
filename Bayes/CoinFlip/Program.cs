using Microsoft.ML.Probabilistic;
using Microsoft.ML.Probabilistic.Algorithms;
using Microsoft.ML.Probabilistic.Math;
using Microsoft.ML.Probabilistic.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using OxyPlot;
using SkiaSharp;
using OxyPlot.Series;
using Microsoft.ML.Probabilistic.Distributions;
using OxyPlot.Wpf;



//Variable<bool> firstCoin = Variable.Bernoulli(0.5);
//Variable<bool> secondCoin = Variable.Bernoulli(0.5);

//Variable<bool> bothHead = firstCoin & secondCoin;
//Variable<bool> diffrence = firstCoin == true & secondCoin == false;
//bothHead.ObservedValue = false;

//InferenceEngine engine = new InferenceEngine();
//Console.WriteLine("P(bothHead | firstCoin = true, secondCoin = true) = " + engine.Infer(bothHead));
//Console.WriteLine("P(bothHead | firstCoin = true, secondCoin = false) = " + engine.Infer(diffrence));

//Variable<double> x2 = Variable.GaussianFromMeanAndVariance(0, 1).Named("x2");
//Variable.ConstrainTrue(x2 > 0.5);

//InferenceEngine engine = new InferenceEngine();
//engine.Algorithm = new ExpectationPropagation();
//Console.WriteLine("Dist ober x=" + engine.Infer(x2));

//for (double thresh = 0; thresh <= 1; thresh += 0.1)
//{
//    Variable<double> x = Variable.GaussianFromMeanAndVariance(0, 1).Named("x");
//    Variable.ConstrainTrue(x > thresh);
//    engine.Algorithm = new ExpectationPropagation();
//    Console.WriteLine("Dist over x given thresh of " + thresh + "=" + engine.Infer(x));
//}


//class Program
//{
//    static void Main(string[] args)
//    {
//        Variable<bool>[] data = new Variable<bool>[100];
//        for (int i = 0; i < data.Length; i++)
//        {
//            // Simulate data from a Bernoulli distribution
//            data[i] = Variable.Bernoulli(0.5);
//        }

//        Variable<double> mean = Variable.GaussianFromMeanAndVariance(0, 1).Named("mean");
//        Variable<double> precision = Variable.GammaFromShapeAndScale(1, 1).Named("variance");

//        InferenceEngine engine = new InferenceEngine();

//        List<double> inferredMeans = new List<double>();
//        List<double> inferredPrecisions = new List<double>();

//        for (int i = 0; i < data.Length; i++)
//        {
//            data[i].ObservedValue = true;
//            Variable<double> x = Variable.GaussianFromMeanAndPrecision(mean, precision);
//            engine.Infer(data[i]);
//            if (data[i].ObservedValue)
//                x.ObservedValue = 1.0;
//            else
//                x.ObservedValue = 0.0;

//            inferredMeans.Add(((Gaussian)engine.Infer(mean)).GetMean());
//            inferredPrecisions.Add(((Gamma)engine.Infer(precision)).GetMean());
//        }

//        Console.WriteLine("mean=" + engine.Infer(mean));
//        Console.WriteLine("prec=" + engine.Infer(precision));
//        engine.ShowFactorGraph = true;

//        // Generate graphs
//        GenerateGraph("Inferred Means", "Iteration", "Mean", inferredMeans);
//        GenerateGraph("Inferred Precisions", "Iteration", "Precision", inferredPrecisions);
//    }

//    static void GenerateGraph(string title, string xAxisTitle, string yAxisTitle, List<double> data)
//    {
//        var plotModel = new PlotModel { Title = title };
//        plotModel.Axes.Add(new OxyPlot.Axes.LinearAxis { Position = OxyPlot.Axes.AxisPosition.Bottom, Title = xAxisTitle });
//        plotModel.Axes.Add(new OxyPlot.Axes.LinearAxis { Position = OxyPlot.Axes.AxisPosition.Left, Title = yAxisTitle });

//        var series = new LineSeries();
//        for (int i = 0; i < data.Count; i++)
//        {
//            series.Points.Add(new DataPoint(i, data[i]));
//        }

//        plotModel.Series.Add(series);

//        using (var stream = new System.IO.FileStream($"{title}.png", System.IO.FileMode.Create))
//        {
//            var exporter = new OxyPlot.SkiaSharp.PngExporter { Width = 800, Height = 600 };
//            exporter.Export(plotModel, stream);
//        }
//    }
//}

using System;
using System.Collections.Generic;
using System.Text;

Variable<bool> firstCoin = Variable.Bernoulli(0.5).Named("firstCoin"); 
Variable<bool> secondCoin = Variable.Bernoulli(0.5).Named("secondCoin"); 
Variable<bool> bothHeads = (firstCoin & secondCoin).Named("bothHeads"); 
InferenceEngine ie = new InferenceEngine();
ie.SaveFactorGraphToFolder = "engine";
ie.ShowFactorGraph = true;
if (!(ie.Algorithm is VariationalMessagePassing))
{
    Console.WriteLine("Probability both coins are heads: " + ie.Infer(bothHeads));
    bothHeads.ObservedValue = false;
    Console.WriteLine("Probability distribution over firstCoin: " + ie.Infer(firstCoin));
}
else
    Console.WriteLine("This example does not run with Variational Message Passing");
