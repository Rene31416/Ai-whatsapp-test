import * as cdk from "aws-cdk-lib/core";
import { Function, Runtime, Code, LayerVersion } from "aws-cdk-lib/aws-lambda";
import { Construct } from "constructs";
import path from "path";
// import * as sqs from 'aws-cdk-lib/aws-sqs';

export class PyAgentStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);
    const depsLayer = new LayerVersion(this, "DepsLayer", {
      code: Code.fromAsset(
        path.join(__dirname, "../src/lambdas/dependencies/deps")
      ),
      compatibleRuntimes: [Runtime.PYTHON_3_12],
    });

    const lambda = new Function(this, "python-lambda", {
      functionName: "my-python-service",
      runtime: Runtime.PYTHON_3_12,
      handler: "agentLambda.main.handler",
      code: Code.fromAsset("src/lambdas/dist/lambda_function.zip"),
      layers: [depsLayer],
    });
    // The code that defines your stack goes here

    // example resource
    // const queue = new sqs.Queue(this, 'PyAgentQueue', {
    //   visibilityTimeout: cdk.Duration.seconds(300)
    // });
  }
}
